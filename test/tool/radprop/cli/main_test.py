import unittest
from argparse import ArgumentParser

from fiduceo.tool.cli import fetch_std_streams
from fiduceo.tool.radprop.cli.main import _configure_argument_parser
from fiduceo.tool.radprop.cli.main import main


class RadPropCliTest(unittest.TestCase):
    # @todo 2 need to consider if we require this test - if so, implement adapter to shield algorithm from being invoked tb 2018-03-27
    # def test_main_success(self):
    #     with fetch_std_streams() as (stdout, stderr):
    #         status = main(['-i', '/home/pippo/test.nc'])
    #     self.assertEqual(status, 0)
    #     self.assertEqual(stdout.getvalue(), "Running with input file: /home/pippo/test.nc\n")
    #     self.assertEqual(stderr.getvalue(), "")

    def test_main_failure(self):
        with fetch_std_streams() as (stdout, stderr):
            status = main(['-i'])

        self.assertEqual(status, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "usage: fiduceo-radprop [-h] [-v] [--traceback] [--license] [--docs]\n"
                                            "                       [-i INPUT_FILE] [-o OUT_DIR] [-a ALGORITHM]\n"
                                            "fiduceo-radprop: error: argument -i/--input_file: expected one argument\n\n")

    def test_main_license(self):
        with fetch_std_streams() as (stdout, stderr):
            status = main(['--license'])
        self.assertEqual(status, 0)
        self.assertTrue("This program is free software; you can redistribute it and/or modify it" in stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    def test_configure_argument_parser(self):
        parser = ArgumentParser()

        _configure_argument_parser(parser)

        self.assertEqual("Radiance Uncertainty Propagation Tool", parser.description)
        self.assertEqual(4, len(parser._positionals._actions))

        self.assertEqual(['-h', '--help'], parser._positionals._actions[0].option_strings)
        self.assertEqual("help", parser._positionals._actions[0].dest)

        self.assertEqual(['-i', '--input_file'], parser._positionals._actions[1].option_strings)
        self.assertEqual("input_file", parser._positionals._actions[1].dest)

        self.assertEqual(['-o', '--out_dir'], parser._positionals._actions[2].option_strings)
        self.assertEqual("out_dir", parser._positionals._actions[2].dest)
        self.assertEqual("The processing output directory, defaults to .", parser._positionals._actions[2].help)
        self.assertEqual(".", parser._positionals._actions[2].default)

        self.assertEqual(['-a', '--algorithm'], parser._positionals._actions[3].option_strings)
        self.assertEqual("algorithm", parser._positionals._actions[3].dest)
        self.assertEqual("available algorithms are:\n"
                     "- AVHRR_SST_NAIVE\n"
                     "- AVHRR_SST_SIMPLE\n"
                     "- AVHRR_NDVI\n"
                     "- MW_UTH\n", parser._positionals._actions[3].help)


