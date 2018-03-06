import argparse
import os

import xarray as xr

from fiduceo.tool.radprop.algorithms.algorithm_factory import AlgorithmFactory


class RadPropProcessor():

    def __init__(self):
        self._algorithm_factory = AlgorithmFactory()
        self.input_file = None

    def run(self, args):
        cmd_line_args = self._parse_cmd_line(args)

        dataset = xr.open_dataset(cmd_line_args.input_file, chunks=1024*1024)

        algorithm = self._algorithm_factory.get_algorithm(cmd_line_args.algorithm)
        # @todo 1 tb/tb check variables 2018-03-06
        target_variable = algorithm.process(dataset)

        target_dataset = xr.Dataset()
        target_dataset[cmd_line_args.algorithm] = target_variable

        self._write_result(cmd_line_args, target_dataset)

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

    def _parse_cmd_line(self, args):
        cmd_line_parser = self._create_cmd_line_parser()
        cmd_line_args = cmd_line_parser.parse_args(args)

        if not os.path.isfile(cmd_line_args.input_file):
            raise IOError("Input file does not exist: " + cmd_line_args.input_file)

        return cmd_line_args

    def _create_cmd_line_parser(self):
        # @todo 3 tb/tb add version number to description 2018-03-05
        parser = argparse.ArgumentParser(description='Radiance Uncertainty Propagation Tool')
        parser.add_argument('input_file')

        algorithm_names = self._algorithm_factory.get_names()
        help_string = "available algorithms are:\n"
        for name in algorithm_names:
            help_string += "- " + name + "\n"
        parser.add_argument("-a", "--algorithm", help=help_string)

        parser.add_argument("-o", "--out_dir", default=".", help="The processing output directory, defaults to .")

        return parser

    @staticmethod
    def _create_target_filename(source_file_name, algorithm_name):
        (head, file_name) = os.path.split(source_file_name)
        (prefix, extension) = os.path.splitext(file_name)

        return prefix +"_" + algorithm_name + extension
