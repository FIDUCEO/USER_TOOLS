import unittest

from fiduceo.tool.cli import run_main, CliError, fetch_std_streams


def _invoke_tool(args_obj):
    if args_obj.format_name == 'word':
        # Intentional failure
        raise CliError(33, 'No, not Word please!')
    if args_obj.format_name == 'geotiff':
        # Simulate unhandled I/O error
        raise IOError('illegal format')
    print("Biboized it.")


def _configure_argument_parser(argument_parser):
    #
    # add tool-specific arguments here...
    #
    argument_parser.add_argument('-f', '--format', dest='format_name', metavar='FORMAT',
                                 help='output file format')


CLI_CONFIG = dict(name="bibo", version="0.5", description="Biboizer Tool",
                  licence_text='"THE BEER-WARE LICENSE" (Revision 42)',
                  docs_url='https://github.com/bibo')


class CliRunMainTest(unittest.TestCase):
    def test_print_help(self):
        with fetch_std_streams() as (stdout, stderr):
            status = run_main(CLI_CONFIG, _configure_argument_parser, ['--help'], _invoke_tool)
        self.assertEqual(status, 0)
        self.assertTrue(stdout.getvalue().startswith('usage: bibo ['))
        self.assertTrue('Biboizer Tool, version 0.5' in stdout.getvalue())
        self.assertEqual(stderr.getvalue(), '')

    def test_print_version(self):
        with fetch_std_streams() as (stdout, stderr):
            status = run_main(CLI_CONFIG, _configure_argument_parser, ['--version'], _invoke_tool)
        self.assertEqual(status, 0)
        self.assertEqual(stdout.getvalue(), 'bibo 0.5\n')
        self.assertEqual(stderr.getvalue(), '')

    def test_invoke_success(self):
        with fetch_std_streams() as (stdout, stderr):
            status = run_main(CLI_CONFIG, _configure_argument_parser, ['-f', 'netcdf'], _invoke_tool)
        self.assertEqual(status, 0)
        self.assertEqual(stdout.getvalue(), 'Biboized it.\n')
        self.assertEqual(stderr.getvalue(), '')

    def test_invoke_fails_intentionally(self):
        with fetch_std_streams() as (stdout, stderr):
            status = run_main(CLI_CONFIG, _configure_argument_parser, ['-f', 'word'], _invoke_tool)
        self.assertEqual(status, 33)
        self.assertEqual(stdout.getvalue(), '')
        self.assertEqual(stderr.getvalue(), 'bibo: error: No, not Word please!\n')

    def test_invoke_fails_accidentally(self):
        with fetch_std_streams() as (stdout, stderr):
            status = run_main(CLI_CONFIG, _configure_argument_parser, ['-f', 'geotiff'], _invoke_tool)
        self.assertEqual(status, -1)
        self.assertEqual(stdout.getvalue(), '')
        self.assertEqual(stderr.getvalue(), 'bibo: error: illegal format\n')


class CliErrorTest(unittest.TestCase):
    def test_it(self):
        error = CliError(854, "oops")
        self.assertEqual(error.status, 854)
        self.assertEqual(error.message, "oops")

        error = CliError(854, None)
        self.assertEqual(error.status, 854)
        self.assertEqual(error.message, None)

        with self.assertRaises(ValueError):
            CliError(None, "arg")
