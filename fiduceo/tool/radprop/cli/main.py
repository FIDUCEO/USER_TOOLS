import sys

from fiduceo.tool.cli import run_main

_LICENSE_TEXT = """
                     GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
"""


def _invoke_tool(args_obj):
    # TODO invoke actual tool entry point using args_obj, may raise CliError
    print("Running with input file:", args_obj.input_file)


def _configure_argument_parser(argument_parser):
    #
    # TODO add specific "fiduceo-radprop" arguments here...
    #
    argument_parser.add_argument('-i', '--input_file',
                                 default='',
                                 metavar='INPUT_FILE', help='the input file')


def main(args=None):
    cli_config = dict(
        name='fiduceo-radprop',
        version='0.1.0-dev1',
        description='XYZ uncertainty propagation tool',
        docs_url='https://github.com/FIDUCEO/USER_TOOLS',
        license_text=_LICENSE_TEXT,
    )
    return run_main(cli_config,
                    _configure_argument_parser,
                    args,
                    _invoke_tool)


if __name__ == '__main__':
    sys.exit(main())
