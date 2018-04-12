import os
import unittest

import xarray as xr

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

        dataset = xr.open_dataset(self.target_file, chunks=1024 * 1024)
        try:
            u_total = dataset["u_total"]
            self.assertAlmostEqual(0.40943062, u_total.values[13, 13], 8)

            u_independent = dataset["u_independent"]
            self.assertAlmostEqual(0.058159404, u_independent.values[14, 14], 8)

            u_structured = dataset["u_structured"]
            self.assertAlmostEqual(0.33959532, u_structured.values[15, 15], 8)

            retrieval = dataset["AVHRR_SST_NAIVE"]
            self.assertAlmostEqual(257.85, retrieval.values[16, 16], 8)
        finally:
            dataset.close()

    def test_run_avhrr_simple_sst(self):
        cmd_line_args = ["-o", self.output_dir, "-a", "AVHRR_SST_SIMPLE", "-i", self.test_file]

        main(cmd_line_args)

        self.target_file = os.path.join(self.output_dir, "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_SST_SIMPLE.nc")
        self.assertTrue(os.path.isfile(self.target_file))

        dataset = xr.open_dataset(self.target_file, chunks=1024 * 1024)
        try:
            u_total = dataset["u_total"]
            self.assertAlmostEqual(0.5787318, u_total.values[23, 23], 7)

            u_independent = dataset["u_independent"]
            self.assertAlmostEqual(0.09593465, u_independent.values[24, 24], 8)

            u_structured = dataset["u_structured"]
            self.assertAlmostEqual(0.58060545, u_structured.values[25, 25], 8)

            retrieval = dataset["AVHRR_SST_SIMPLE"]
            self.assertAlmostEqual(265.4596790615258, retrieval.values[26, 26], 8)
        finally:
            dataset.close()

    def test_run_avhrr_ndvi(self):
        cmd_line_args = ["-o", self.output_dir, "-a", "AVHRR_NDVI", "-i", self.test_file]

        main(cmd_line_args)

        self.target_file = os.path.join(self.output_dir, "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_NDVI.nc")
        self.assertTrue(os.path.isfile(self.target_file))

        dataset = xr.open_dataset(self.target_file, chunks=1024 * 1024)
        try:
            u_total = dataset["u_total"]
            self.assertAlmostEqual(0.008686024, u_total.values[33, 33], 8)

            u_independent = dataset["u_independent"]
            self.assertAlmostEqual(0.00013940882, u_independent.values[34, 34], 8)

            u_structured = dataset["u_structured"]
            self.assertAlmostEqual(0.0074526602, u_structured.values[35, 35], 8)

            retrieval = dataset["AVHRR_NDVI"]
            self.assertAlmostEqual(-0.027305512622359675, retrieval.values[36, 36], 8)
        finally:
            dataset.close()
