import sys

from fiduceo.tool.cli import run_main
from fiduceo.tool.radprop.rad_prop_processor import RadPropProcessor
from fiduceo.tool.version import __version__

_LICENSE_TEXT = """
                    Copyright (C) 2018 Brockmann Consult GmbH
  This code was developed for the EC project 'Fidelity and Uncertainty in
  Climate Data Records from Earth Observations (FIDUCEO)'.
  Grant Agreement: 638822
 
  This program is free software; you can redistribute it and/or modify it
  under the terms of the GNU General Public License as published by the Free
  Software Foundation; either version 3 of the License, or (at your option)
  any later version.
  This program is distributed in the hope that it will be useful, but WITHOUT
  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
  FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
  more details.
 
  A copy of the GNU General Public License should have been supplied along
  with this program; if not, see http://www.gnu.org/licenses/
"""

processor = RadPropProcessor()


def main(args=None):
    # @todo 1 tb/tb check with Norman - how can we state here usage name "fiduceo-radprop" while the class is named "main" ??? 2018-03-27
    cli_config = dict(name='fiduceo-radprop', version=__version__, description='Retrieval uncertainty propagation tool', docs_url='https://github.com/FIDUCEO/USER_TOOLS', license_text=_LICENSE_TEXT, )
    return run_main(cli_config, _configure_argument_parser, args, _invoke_tool)


def _invoke_tool(args_obj):
    print("Running with input file:", args_obj.input_file)
    processor.run(args_obj)


def _configure_argument_parser(argument_parser):
    argument_parser.description = "Radiance Uncertainty Propagation Tool"
    argument_parser.add_argument('-i', '--input_file', default='', metavar='INPUT_FILE', help='the input file')
    argument_parser.add_argument("-o", "--out_dir", default=".", help="The processing output directory, defaults to .")
    argument_parser.add_argument("-a", "--algorithm", help=processor.get_algorithm_help_string())


if __name__ == '__main__':
    sys.exit(main())
