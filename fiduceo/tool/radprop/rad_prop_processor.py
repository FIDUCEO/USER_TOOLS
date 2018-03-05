import argparse

from fiduceo.tool.radprop.algorithms.algorithm_factory import AlgorithmFactory


class RadPropProcessor():

    def __init__(self):
        self._algorithm_factory = AlgorithmFactory()

    def run(self, args):
        cmd_line_parser = self._create_cmd_line_parser()
        cmd_line_args = cmd_line_parser.parse_args(args)

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
