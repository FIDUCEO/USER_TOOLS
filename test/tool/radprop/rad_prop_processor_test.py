import unittest

from fiduceo.tool.radprop.rad_prop_processor import RadPropProcessor


class RadPropProcessorTest(unittest.TestCase):

    def test_create_target_file_name(self):
        target_file_name = RadPropProcessor._create_target_filename("FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1.nc", "AVHRR_SST_NAIVE")
        self.assertEqual("FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_SST_NAIVE.nc", target_file_name)
