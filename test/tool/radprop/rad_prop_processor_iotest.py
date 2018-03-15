import os
import unittest

from fiduceo.tool.radprop.rad_prop_processor import RadPropProcessor
from test.tool.test_data_utils import TestDataUtils


class RadPropProcessorIOTest(unittest.TestCase):
    AVHRR_FCDR = "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1.nc"

    def setUp(self):
        self.target_file = None

    def tearDown(self):
        if self.target_file is not None:
            os.remove(self.target_file)

    def test_run_avhrr_simple_sst(self):
        data_dir = TestDataUtils.get_test_data_dir()
        test_file = os.path.join(data_dir, self.AVHRR_FCDR)
        self.assertTrue(os.path.isfile(test_file))

        output_dir = TestDataUtils.get_output_dir()

        cmd_line_args = ["-o", output_dir, "-a", "AVHRR_SST_NAIVE", test_file]

        processor = RadPropProcessor()

        processor.run(cmd_line_args)

        self.target_file = os.path.join(output_dir, "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_SST_NAIVE.nc")
        self.assertTrue(os.path.isfile(self.target_file))
