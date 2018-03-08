"""
Common CLI constants, classes, functions.
"""

import argparse
import io
import sys
import traceback
from contextlib import contextmanager


def run_main(cli_config, configure_argument_parser, args, invoke_tool):
    """
    Configures a CLI, parses CLI arguments, and invokes a CLI tool.

    :param cli_config: CLI configuration.
           A dict-like which must include 'name', 'version', 'description' and may include 'doc_url', 'license_text'.
    :param configure_argument_parser:
           Function that receives an ``argparse.ArgumentParser`` instance to be configured
    :param args: The arguments passed to the CLI
    :param invoke_tool: The actual CLI tool implementation. Receives the parsed arguments.
           May raise ``ExitException`` on failure.
    :return: the status code (integer number) where any non-zero value reports a failure.
    """
    argument_parser = _new_argument_parser(cli_config)

    configure_argument_parser(argument_parser)

    args = sys.argv[1:] if args is None else args
    status, message = 0, None

    try:
        args_obj = argument_parser.parse_args(args)

        if 'license_text' in cli_config and args_obj.license:
            print(cli_config['license_text'])
            return 0

        if 'docs_url' in cli_config and args_obj.docs:
            import webbrowser
            webbrowser.open_new_tab(cli_config['docs_url'])
            return 0

        try:
            invoke_tool(args_obj)
        except CliError as e:
            status, message = e.status, _format_error_message(cli_config, e.message)
        except BaseException as e:
            show_traceback = args_obj.traceback
            if show_traceback:
                traceback.print_exc()
            status, message = -1, _format_error_message(cli_config, str(e))

    except CliError as e:
        status, message = e.status, e.message

    if message:
        if status:
            sys.stderr.write("%s\n" % message)
        else:
            sys.stdout.write("%s\n" % message)

    return status


class CliError(Exception):
    """Used to raise from CLI implementations instead of exiting the current process."""

    def __init__(self, status, message):
        if status is None:
            raise ValueError('status must be given')
        self._status = status
        self._message = message

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        return self._message

    def __str__(self):
        return '%s (%s)' % (self.message, self.status)


def _new_argument_parser(cli_config):
    """
    Create a new ``argparse.ArgumentParser`` using the given tool info.

    :param cli_config: CLI configuration
    :return: a new "argparse.ArgumentParser"
    """
    name, version, description = cli_config['name'], cli_config['version'], cli_config['description']

    parser = _NoExitArgumentParser(prog=name,
                                   description='%s, version %s' % (description, version))

    parser.add_argument('-v', '--version', action='version', version='%s %s' % (name, version))
    parser.add_argument('--traceback', action='store_true',
                        help='show (Python) stack traceback for the last error')
    if 'license_text' in cli_config:
        parser.add_argument('--license', action='store_true',
                            help='show software license and exit')
    if 'docs_url' in cli_config:
        parser.add_argument('--docs', action='store_true',
                            help='show software documentation in a browser window')

    return parser


class _NoExitArgumentParser(argparse.ArgumentParser):
    """
    Special ``argparse.ArgumentParser`` that never directly exits the current process, so we can test our main module.
    It raises an ``CliError`` instead.
    """

    def __init__(self, *args, **kwargs):
        super(_NoExitArgumentParser, self).__init__(*args, **kwargs)

    def exit(self, status=0, message=None):
        """Overrides the base class method in order to raise an ``CliError``."""
        raise CliError(status, message)


@contextmanager
def fetch_std_streams():
    """
    A context manager which can be used to temporarily fetch the standard output streams
    ``sys.stdout`` and  ``sys.stderr``.

    This is very useful for unit-testing.

    Usage:::

        with fetch_std_streams() as stdout, stderr
            sys.stdout.write('yes')
            sys.stderr.write('oh no')
        print('fetched', stdout.getvalue())
        print('fetched', stderr.getvalue())

    :return: yields  ``sys.stdout`` and  ``sys.stderr`` redirected into buffers of type ``StringIO``
    """
    sys.stdout.flush()
    sys.stderr.flush()

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout.flush()
        sys.stderr.flush()

        sys.stdout = old_stdout
        sys.stderr = old_stderr


def _format_error_message(cli_config, message):
    return "%s: error: %s" % (cli_config['name'], message)
