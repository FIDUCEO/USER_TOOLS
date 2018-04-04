import os

import xarray as xr
from xarray import Variable

from fiduceo.tool.radprop.algorithms.algorithm_factory import AlgorithmFactory
from fiduceo.tool.radprop.radiance_disturbances import RadianceDisturbances


class RadPropProcessor():

    def __init__(self):
        self._algorithm_factory = AlgorithmFactory()
        self._rad_disturbance_proc = RadianceDisturbances()
        self.input_file = None

    def run(self, cmd_line_args):
        dataset = xr.open_dataset(cmd_line_args.input_file, chunks=1024 * 1024)

        algorithm = self._algorithm_factory.get_algorithm(cmd_line_args.algorithm)

        variable_names = algorithm.get_variable_names()
        disturbances = self._rad_disturbance_proc.calculate(dataset, variable_names)

        disturbed_dataset = self.calculate_positive_disturbed_dataset(dataset, disturbances, variable_names)
        z2 = algorithm.process(disturbed_dataset)

        disturbed_dataset = self.calculate_negative_disturbed_dataset(dataset, disturbances, variable_names)
        z1 = algorithm.process(disturbed_dataset)

        sens_coeff = (z2 - z1) * 0.5

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
