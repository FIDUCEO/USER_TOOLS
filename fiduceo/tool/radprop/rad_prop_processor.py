import os

import numpy as np
import xarray as xr

from fiduceo.tool.radprop.algorithms.algorithm_factory import AlgorithmFactory
from fiduceo.tool.radprop.radiance_disturbances import RadianceDisturbances
from fiduceo.tool.radprop.sensitivity_calculator import SensitivityCalculator


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
        disturbances = self._rad_disturbance_proc.calculate(dataset, variable_names)

        # sensitivities per channel
        sensitivities = self.sensitivity_calculator.run(dataset, disturbances, algorithm)

        rci, rcs = self._subset_correlation_matrices(dataset, variable_names)

        width = dataset.dims["x"]
        height = dataset.dims["y"]

        for y in range(0, height):
            for x in range(0, width):
                # @todo extract uIndependent for pixel
                # @todo calculate Sci = Uci * Rci * UciT

                # @todo extract uStructured for pixel
                # @todo calculate Scs = Ucs * Rcs * UcsT

                # not for now tb 2018-04-11
                # @todo calculate Sch = Uch + UchT

                sens_pixel = sensitivities[:, y, x]

                # @todo calculate total uncertainty

                # @todo calculate component uncertainty
                pass

        target_variable = algorithm.process(dataset)

        target_dataset = xr.Dataset()
        target_dataset[cmd_line_args.algorithm] = target_variable

        self._write_result(cmd_line_args, target_dataset)

    def get_algorithm_help_string(self):
        algorithm_names = self._algorithm_factory.get_names()
        help_string = "available algorithms are:\n"
        for name in algorithm_names:
            help_string += "- " + name + "\n"

        return help_string

    def _subset_correlation_matrices(self, dataset, channel_names):
        # @todo read correlation matrices and subset
        num_channels = len(channel_names)
        rci = np.diag(np.ones(num_channels))
        rcs = np.diag(np.ones(num_channels))
        return rci, rcs

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
