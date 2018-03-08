import unittest
from fiduceo.tool.radprop.cli.main import main
from fiduceo.tool.cli import fetch_std_streams


class RadPropCliTest(unittest.TestCase):
    def test_main_success(self):
        with fetch_std_streams() as (stdout, stderr):
            status = main(['-i', '/home/pippo/test.nc'])
        self.assertEqual(status, 0)
        self.assertEqual(stdout.getvalue(), "Running with input file: /home/pippo/test.nc\n")
        self.assertEqual(stderr.getvalue(), "")

    def test_main_failure(self):
        with fetch_std_streams() as (stdout, stderr):
            status = main(['-i'])

        self.assertEqual(status, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(),
                         "usage: fiduceo-radprop [-h] [-v] [--traceback] [--license] [--docs]\n"
                         "                       [-i INPUT_FILE]\n"
                         "fiduceo-radprop: error: argument -i/--input_file: expected one argument\n\n")

    def test_main_license(self):
        with fetch_std_streams() as (stdout, stderr):
            status = main(['--license'])
        self.assertEqual(status, 0)
        self.assertTrue("GNU GENERAL PUBLIC LICENSE" in stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")
