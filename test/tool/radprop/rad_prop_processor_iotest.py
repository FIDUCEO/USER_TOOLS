import os
import unittest

import xarray as xr

from fiduceo.tool.radprop.cli.main import main
from test.tool.test_data_utils import TestDataUtils


class RadPropProcessorIOTest(unittest.TestCase):
    AVHRR_FCDR = "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1.nc"
    MHS_FCDR = "FIDUCEO_FCDR_L1C_MHS_METOPB_20150706154758_20150706172920_EASY_v2.0_fv1.1.4.nc"

    def setUp(self):
        self.target_file = None

        self.output_dir = TestDataUtils.get_output_dir()

    def _get_test_file(self, filename):
        data_dir = TestDataUtils.get_test_data_dir()
        test_file = os.path.join(data_dir, filename)
        self.assertTrue(os.path.isfile(test_file))
        return test_file

    def tearDown(self):
        if self.target_file is not None:
            os.remove(self.target_file)

    def test_run_avhrr_naive_sst(self):
        test_file = self._get_test_file(self.AVHRR_FCDR)

        cmd_line_args = ["-o", self.output_dir, "-a", "AVHRR_SST_NAIVE", "-i", test_file, "--traceback"]

        main(cmd_line_args)

        self.target_file = os.path.join(self.output_dir, "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_SST_NAIVE.nc")
        self.assertTrue(os.path.isfile(self.target_file))

        dataset = xr.open_dataset(self.target_file, chunks=1024 * 1024)
        try:
            u_total = dataset["u_total"]
            self.assertAlmostEqual(0.40943062, u_total.values[13, 13], 8)
            self.assertAlmostEqual(0.4274388, u_total.values[14, 14], 8)

            u_independent = dataset["u_independent"]
            self.assertAlmostEqual(0.058159404, u_independent.values[14, 14], 8)
            self.assertAlmostEqual(0.061891206, u_independent.values[15, 15], 8)

            u_structured = dataset["u_structured"]
            self.assertAlmostEqual(0.33959532, u_structured.values[15, 15], 8)
            self.assertAlmostEqual(0.3428737, u_structured.values[16, 16], 7)

            u_common = dataset["u_common"]
            self.assertAlmostEqual(0.0, u_common.values[55, 35], 8)
            self.assertAlmostEqual(0.0, u_common.values[56, 36], 8)

            retrieval = dataset["AVHRR_SST_NAIVE"]
            self.assertAlmostEqual(257.85, retrieval.values[16, 16], 8)
            self.assertAlmostEqual(260.28, retrieval.values[17, 17], 8)
        finally:
            dataset.close()

    def test_run_avhrr_simple_sst(self):
        test_file = self._get_test_file(self.AVHRR_FCDR)
        cmd_line_args = ["-o", self.output_dir, "-a", "AVHRR_SST_SIMPLE", "-i", test_file, "--traceback"]

        main(cmd_line_args)

        self.target_file = os.path.join(self.output_dir, "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_SST_SIMPLE.nc")
        self.assertTrue(os.path.isfile(self.target_file))

        dataset = xr.open_dataset(self.target_file, chunks=1024 * 1024)
        try:
            u_total = dataset["u_total"]
            self.assertAlmostEqual(0.5787318, u_total.values[23, 23], 7)
            self.assertAlmostEqual(0.54311913, u_total.values[24, 24], 8)

            u_independent = dataset["u_independent"]
            self.assertAlmostEqual(0.09593465, u_independent.values[24, 24], 8)
            self.assertAlmostEqual(0.09226596, u_independent.values[25, 25], 8)

            u_structured = dataset["u_structured"]
            self.assertAlmostEqual(0.58060545, u_structured.values[25, 25], 8)
            self.assertAlmostEqual(0.56661135, u_structured.values[26, 26], 8)

            u_common = dataset["u_common"]
            self.assertAlmostEqual(0.0, u_common.values[55, 35], 8)
            self.assertAlmostEqual(0.0, u_common.values[56, 36], 8)

            retrieval = dataset["AVHRR_SST_SIMPLE"]
            self.assertAlmostEqual(265.4596790615258, retrieval.values[26, 26], 8)
            self.assertAlmostEqual(255.90638957876251, retrieval.values[27, 27], 8)
        finally:
            dataset.close()

    def test_run_avhrr_ndvi(self):
        test_file = self._get_test_file(self.AVHRR_FCDR)
        cmd_line_args = ["-o", self.output_dir, "-a", "AVHRR_NDVI", "-i", test_file, "--traceback"]

        main(cmd_line_args)

        self.target_file = os.path.join(self.output_dir, "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_NDVI.nc")
        self.assertTrue(os.path.isfile(self.target_file))

        dataset = xr.open_dataset(self.target_file, chunks=1024 * 1024)
        try:
            u_total = dataset["u_total"]
            self.assertAlmostEqual(0.008686024, u_total.values[33, 33], 8)
            self.assertAlmostEqual(0.011701324, u_total.values[34, 34], 8)

            u_independent = dataset["u_independent"]
            self.assertAlmostEqual(0.00013940882, u_independent.values[34, 34], 8)
            self.assertAlmostEqual(8.8693334e-05, u_independent.values[35, 35], 8)

            u_structured = dataset["u_structured"]
            self.assertAlmostEqual(0.0074526602, u_structured.values[35, 35], 8)
            self.assertAlmostEqual(0.0071001686, u_structured.values[36, 36], 8)

            u_common = dataset["u_common"]
            self.assertAlmostEqual(0.0, u_common.values[55, 35], 8)
            self.assertAlmostEqual(0.0, u_common.values[56, 36], 8)

            retrieval = dataset["AVHRR_NDVI"]
            self.assertAlmostEqual(-0.027305512622359675, retrieval.values[36, 36], 8)
            self.assertAlmostEqual(-0.0225967062428188, retrieval.values[37, 37], 8)
        finally:
            dataset.close()

    def test_run_mhs_uth(self):
        test_file = self._get_test_file(self.MHS_FCDR)
        cmd_line_args = ["-o", self.output_dir, "-a", "MW_UTH", "-i", test_file, "--traceback"]

        main(cmd_line_args)

        self.target_file = os.path.join(self.output_dir, "FIDUCEO_FCDR_L1C_MHS_METOPB_20150706154758_20150706172920_EASY_v2.0_fv1.1.4_MW_UTH.nc")
        self.assertTrue(os.path.isfile(self.target_file))

        dataset = xr.open_dataset(self.target_file, chunks=1024 * 1024)
        try:
            u_total = dataset["u_total"]
            self.assertAlmostEqual(0.0021023436, u_total.values[43, 33], 8)
            self.assertAlmostEqual(0.0020873963, u_total.values[44, 34], 8)

            u_independent = dataset["u_independent"]
            self.assertAlmostEqual(0.0017900737, u_independent.values[44, 34], 8)
            self.assertAlmostEqual(0.0017788752, u_independent.values[45, 35], 8)

            u_structured = dataset["u_structured"]
            self.assertAlmostEqual(0.0007277601, u_structured.values[45, 35], 8)
            self.assertAlmostEqual(0.0007683263, u_structured.values[46, 36], 8)

            u_common = dataset["u_common"]
            self.assertAlmostEqual(0.00075336185, u_common.values[55, 35], 8)
            self.assertAlmostEqual(0.0006663381, u_common.values[56, 36], 8)

            retrieval = dataset["MW_UTH"]
            self.assertAlmostEqual(0.12945784138444968, retrieval.values[46, 36], 8)
            self.assertAlmostEqual(0.12526797955225227, retrieval.values[47, 37], 8)
        finally:
            dataset.close()