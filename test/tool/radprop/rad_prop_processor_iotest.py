import os
import unittest

from fiduceo.tool.radprop.cli.main import main
from test.tool.test_data_utils import TestDataUtils


class RadPropProcessorIOTest(unittest.TestCase):
    AVHRR_FCDR = "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1.nc"

    def setUp(self):
        self.target_file = None

        data_dir = TestDataUtils.get_test_data_dir()
        self.test_file = os.path.join(data_dir, self.AVHRR_FCDR)
        self.assertTrue(os.path.isfile(self.test_file))

        self.output_dir = TestDataUtils.get_output_dir()

    def tearDown(self):
        if self.target_file is not None:
            os.remove(self.target_file)

    def test_run_avhrr_naive_sst(self):
        cmd_line_args = ["-o", self.output_dir, "-a", "AVHRR_SST_NAIVE", "-i", self.test_file]

        main(cmd_line_args)

        self.target_file = os.path.join(self.output_dir, "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_SST_NAIVE.nc")
        self.assertTrue(os.path.isfile(self.target_file))

    def test_run_avhrr_simple_sst(self):
        cmd_line_args = ["-o", self.output_dir, "-a", "AVHRR_SST_SIMPLE", "-i", self.test_file]

        main(cmd_line_args)

        self.target_file = os.path.join(self.output_dir, "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_SST_SIMPLE.nc")
        self.assertTrue(os.path.isfile(self.target_file))

    def test_run_avhrr_ndvi(self):
        cmd_line_args = ["-o", self.output_dir, "-a", "AVHRR_NDVI", "-i", self.test_file]

        main(cmd_line_args)

        self.target_file = os.path.join(self.output_dir, "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_NDVI.nc")
        self.assertTrue(os.path.isfile(self.target_file))
