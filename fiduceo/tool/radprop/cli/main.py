import sys

from fiduceo.tool.cli import run_main

_LICENSE_TEXT = """
The MIT License (MIT)

Copyright (c) 2018 FIDUCEO User Tools

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
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
