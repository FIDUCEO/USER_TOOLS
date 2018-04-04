import os

import numpy as np
import xarray as xr
from xarray import Variable

from fiduceo.tool.radprop.algorithms.algorithm_factory import AlgorithmFactory


class RadPropProcessor():

    def __init__(self):
        self._algorithm_factory = AlgorithmFactory()
        self.input_file = None

    def run(self, cmd_line_args):
        dataset = xr.open_dataset(cmd_line_args.input_file, chunks=1024 * 1024)

        algorithm = self._algorithm_factory.get_algorithm(cmd_line_args.algorithm)

        variable_names = algorithm.get_variable_names()
        disturbances = self._calculate_radiance_disturbances(dataset, variable_names)

        disturbed_dataset = self.calculate_positive_disturbed_dataset(dataset, disturbances, variable_names)
        z2 = algorithm.process(disturbed_dataset)

        disturbed_dataset = self.calculate_negative_disturbed_dataset(dataset, disturbances, variable_names)
        z1 = algorithm.process(disturbed_dataset)

        sens_coeff = (z2 - z1) * 0.5
        print(sens_coeff[0,0])


        target_variable = algorithm.process(dataset)

        target_dataset = xr.Dataset()
        target_dataset[cmd_line_args.algorithm] = target_variable

        self._write_result(cmd_line_args, target_dataset)

    def calculate_positive_disturbed_dataset(self, dataset, disturbances, variable_names):
        disturbed_dataset = xr.Dataset()
        for variable_name in variable_names:
            variable = dataset[variable_name]
            if variable_name in disturbances:
                rad_dist = variable.data + disturbances[variable_name]
                disturbed_dataset[variable_name] = Variable(variable.dims, rad_dist)
            else:
                disturbed_dataset[variable_name] = variable
        return disturbed_dataset

    def calculate_negative_disturbed_dataset(self, dataset, disturbances, variable_names):
        disturbed_dataset = xr.Dataset()
        for variable_name in variable_names:
            variable = dataset[variable_name]
            if variable_name in disturbances:
                rad_dist = variable.data - disturbances[variable_name]
                disturbed_dataset[variable_name] = Variable(variable.dims, rad_dist)
            else:
                disturbed_dataset[variable_name] = variable
        return disturbed_dataset

    def get_algorithm_help_string(self):
        algorithm_names = self._algorithm_factory.get_names()
        help_string = "available algorithms are:\n"
        for name in algorithm_names:
            help_string += "- " + name + "\n"

        return help_string

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

    @staticmethod
    def _calculate_radiance_disturbances(dataset, variable_names):
        disturbances = dict()

        y = dataset.dims["y"]
        x = dataset.dims["x"]
        for variable_name in variable_names:
            u_ind_name = "u_independent_" + variable_name

            u_ind = None
            if u_ind_name in dataset:
                u_ind = dataset[u_ind_name].data

            u_str_name = "u_structured_" + variable_name
            u_str = None
            if u_str_name in dataset:
                u_str = dataset[u_str_name].data

            u_com_name = "u_common_" + variable_name
            u_com = None
            if u_com_name in dataset:
                u_com = dataset[u_com_name].data

            if u_str is None and u_ind is None and u_com is None:
                continue    # if no uncertainty can be found we skip this variable from calculation tb 2018-04-04

            if u_ind is None:
                u_ind = np.zeros([y, x])

            if u_str is None:
                u_str = np.zeros([y, x])

            if u_com is None:
                u_com = np.zeros([y, x])

            rad_delta = np.sqrt(u_ind * u_ind + u_str * u_str + u_com * u_com)
            disturbances.update({variable_name : rad_delta})

        return disturbances
