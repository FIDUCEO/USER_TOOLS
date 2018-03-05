import unittest

from test.tool.test_data_utils import TestDataUtils


class RadPropProcessorIOTest(unittest.TestCase):

    def test_run(self):
        data_dir = TestDataUtils.get_test_data_dir()
