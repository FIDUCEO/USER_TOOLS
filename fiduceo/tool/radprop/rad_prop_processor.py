import os

import numpy as np
import xarray as xr
from xarray import Variable

from fiduceo.tool.radprop.algorithms.algorithm_factory import AlgorithmFactory
from fiduceo.tool.radprop.radiance_disturbances import RadianceDisturbances
from fiduceo.tool.radprop.sensitivity_calculator import SensitivityCalculator
from fiduceo.tool.radprop.error_covariances import ErrorCovariances


class RadPropProcessor():

    def __init__(self):
        self._algorithm_factory = AlgorithmFactory()
        self._rad_disturbance_proc = RadianceDisturbances()
        self.sensitivity_calculator = SensitivityCalculator()
        self.input_file = None

    def run(self, cmd_line_args):
        dataset = xr.open_dataset(cmd_line_args.input_file, chunks=1024 * 1024)

        algorithm = self._algorithm_factory.get_algorithm(cmd_line_args.algorithm)

        # disturbances per channel
        variable_names = algorithm.get_variable_names()
        channel_names = self._extract_channel_variables(variable_names)
        disturbances = self._rad_disturbance_proc.calculate(dataset, variable_names)

        # sensitivities per channel
        sensitivities = self.sensitivity_calculator.run(dataset, disturbances, algorithm)

        rci, rcs = self._subset_correlation_matrices(dataset)
        u_ind, u_str = self._extract_uncertainties(dataset, channel_names)

        width = dataset.dims["x"]
        height = dataset.dims["y"]

        u = np.full([height, width], np.nan, np.float32)
        u_i = np.full([height, width], np.nan, np.float32)
        u_s = np.full([height, width], np.nan, np.float32)

        error_covariances = ErrorCovariances()

        for y in range(0, height):
            for x in range(0, width):
                u_ind_pixel = u_ind[:, y, x]
                sci = error_covariances.calculate(u_ind_pixel, rci)

                u_str_pixel = u_str[:, y, x]
                scs = error_covariances.calculate(u_str_pixel, rci)

                # not for now tb 2018-04-11
                # @todo calculate Sch = Uch + UchT

                c = sensitivities[:, y, x]

                u_total_sq = np.dot(c, (sci + scs))
                u_total_sq = np.dot(u_total_sq, c)
                u[y, x] = np.sqrt(u_total_sq)

                u_ind_sq = np.dot(c, sci)
                u_ind_sq = np.dot(u_ind_sq, c)
                u_i[y, x] = np.sqrt(u_ind_sq)

                u_str_sq = np.dot(c, scs)
                u_str_sq = np.dot(u_str_sq, c)
                u_s[y, x] = np.sqrt(u_str_sq)

        target_variable = algorithm.process(dataset)

        target_dataset = xr.Dataset()
        target_dataset[cmd_line_args.algorithm] = target_variable
        target_dataset["u_total"] = Variable(["y", "x"], u)
        target_dataset["u_independent"] = Variable(["y", "x"], u_i)
        target_dataset["u_structured"] = Variable(["y", "x"], u_s)

        self._write_result(cmd_line_args, target_dataset)

        dataset.close()

    def get_algorithm_help_string(self):
        algorithm_names = self._algorithm_factory.get_names()
        help_string = "available algorithms are:\n"
        for name in algorithm_names:
            help_string += "- " + name + "\n"

        return help_string

    def _subset_correlation_matrices(self, dataset):
        # @todo read correlation matrices and subset
        # for now we have only algorithms with two channels and assume no correlation, just to get the code running
        rci = np.diag(np.ones(2))
        rcs = np.diag(np.ones(2))

        # rci = np.array(([1, 0.33], [0.33, 1]), dtype=np.float64)
        # rcs = np.array(([1, 0.33], [0.33, 1]), dtype=np.float64)
        return rci, rcs

    def _extract_uncertainties(self, dataset, channel_names):
        width = dataset.dims["x"]
        height = dataset.dims["y"]
        u_ind = np.full([len(channel_names), height, width], np.nan, np.float64)
        u_str = np.full([len(channel_names), height, width], np.nan, np.float64)

        index = 0
        for name, chanel_index in channel_names.items():
            u_ind_name = "u_independent_" + name
            u_ind[index, :, :] = dataset[u_ind_name].data

            u_str_name = "u_structured_" + name
            u_str[index, :, :] = dataset[u_str_name].data
            index += 1

        return u_ind, u_str

    def _extract_channel_variables(self, variable_names):
        # @todo read from channel coordinate and order by spectral index
        channel_names = dict()
        for name in variable_names:
            if name == "Ch1":
                channel_names.update({"Ch1": 0})
            if name == "Ch2":
                channel_names.update({"Ch2": 1})
            if name == "Ch3a":
                channel_names.update({"Ch3a": 2})
            if name == "Ch3b":
                channel_names.update({"Ch3b": 3})
            if name == "Ch4":
                channel_names.update({"Ch4": 4})
            if name == "Ch5":
                channel_names.update({"Ch5": 5})

        return channel_names

    def _write_result(self, cmd_line_args, target_dataset):
        target_filename = self._create_target_filename(cmd_line_args.input_file, cmd_line_args.algorithm)
        target_path = os.path.join(cmd_line_args.out_dir, target_filename)

        comp = dict(zlib=True, complevel=5)
        encoding = dict()
        for var_name in target_dataset.data_vars:
            var_encoding = dict(comp)
            var_encoding.update(target_dataset[var_name].encoding)
            encoding.update({var_name: var_encoding})
        target_dataset.to_netcdf(target_path, format='netCDF4', engine='netcdf4', encoding=encoding)

    @staticmethod
    def _create_target_filename(source_file_name, algorithm_name):
        (head, file_name) = os.path.split(source_file_name)
        (prefix, extension) = os.path.splitext(file_name)

        return prefix + "_" + algorithm_name + extension
