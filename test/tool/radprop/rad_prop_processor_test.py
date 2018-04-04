import unittest

import numpy as np
import xarray as xr
from xarray import Variable

from fiduceo.tool.radprop.rad_prop_processor import RadPropProcessor


class RadPropProcessorTest(unittest.TestCase):

    def test_create_target_file_name(self):
        target_file_name = RadPropProcessor._create_target_filename("FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1.nc", "AVHRR_SST_NAIVE")
        self.assertEqual("FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_SST_NAIVE.nc", target_file_name)

    def test_calculate_radiance_disturbances_MHS_one_channel(self):
        dataset = xr.Dataset()

        u_ind_ch3_data = np.asarray([[108, 79], [120, 22], [120, 15]]) * 0.01
        dataset["u_independent_Ch3_BT"] = Variable(["y", "x"], u_ind_ch3_data)

        u_str_ch3_data = np.asarray([[118, 89], [130, 32], [130, 25]]) * 0.01
        dataset["u_structured_Ch3_BT"] = Variable(["y", "x"], u_str_ch3_data)

        u_com_ch3_data = np.asarray([[18, 49], [30, 12], [30, 15]]) * 0.01
        dataset["u_common_Ch3_BT"] = Variable(["y", "x"], u_com_ch3_data)

        channels = ["Ch3_BT"]

        disturbances = RadPropProcessor._calculate_radiance_disturbances(dataset, channels)
        self.assertEqual(1, len(disturbances))

        dist_data = disturbances["Ch3_BT"]
        self.assertAlmostEqual(1.6097204726287107, dist_data[0, 0], 8)
        self.assertAlmostEqual(1.2869731931940152, dist_data[0, 1], 8)

    def test_calculate_radiance_disturbances_AVHRR_one_channel(self):
        dataset = xr.Dataset()

        u_ind_ch4_data = np.asarray([[108, 79], [120, 22], [120, 15]]) * 0.01
        dataset["u_independent_Ch4"] = Variable(["y", "x"], u_ind_ch4_data)

        u_str_ch4_data = np.asarray([[118, 89], [130, 32], [130, 25]]) * 0.01
        dataset["u_structured_Ch4"] = Variable(["y", "x"], u_str_ch4_data)

        channels = ["Ch4"]

        disturbances = RadPropProcessor._calculate_radiance_disturbances(dataset, channels)
        self.assertEqual(1, len(disturbances))

        dist_data = disturbances["Ch4"]
        self.assertAlmostEqual(1.5996249560443847, dist_data[0, 0], 8)
        self.assertAlmostEqual(1.1900420160649792, dist_data[0, 1], 8)

    def test_calculate_radiance_disturbances_AMSUB_two_channels(self):
        dataset = xr.Dataset()

        u_ind_ch17_data = np.asarray([[1, 2], [3, 4], [5, 6]]) * 0.01
        dataset["u_independent_Ch17_BT"] = Variable(["y", "x"], u_ind_ch17_data)

        u_str_ch17_data = np.asarray([[7, 8], [9, 10], [11, 12]]) * 0.01
        dataset["u_structured_Ch17_BT"] = Variable(["y", "x"], u_str_ch17_data)

        u_com_ch17_data = np.asarray([[13, 14], [15, 16], [17, 18]]) * 0.01
        dataset["u_common_Ch7_BT"] = Variable(["y", "x"], u_com_ch17_data)

        u_ind_ch18_data = np.asarray([[19, 20], [21, 22], [23, 24]]) * 0.01
        dataset["u_independent_Ch18_BT"] = Variable(["y", "x"], u_ind_ch18_data)

        u_str_ch18_data = np.asarray([[25, 26], [27, 28], [29, 30]]) * 0.01
        dataset["u_structured_Ch18_BT"] = Variable(["y", "x"], u_str_ch18_data)

        u_com_ch18_data = np.asarray([[31, 32], [33, 34], [35, 36]]) * 0.01
        dataset["u_common_Ch18_BT"] = Variable(["y", "x"], u_com_ch18_data)

        channels = ["Ch17_BT", "Ch18_BT"]

        disturbances = RadPropProcessor._calculate_radiance_disturbances(dataset, channels)
        self.assertEqual(2, len(disturbances))

        dist_data = disturbances["Ch17_BT"]
        self.assertAlmostEqual(0.09486832980505137, dist_data[1, 0], 8)
        self.assertAlmostEqual(0.1077032961426901, dist_data[1, 1], 8)

        dist_data = disturbances["Ch18_BT"]
        self.assertAlmostEqual(0.4923413450036469, dist_data[1, 1], 8)
        self.assertAlmostEqual(0.5264978632435273, dist_data[2, 1], 8)

    def test_calculate_radiance_disturbances_AVHRR_three_channels_with_angles(self):
        dataset = xr.Dataset()

        u_ind_ch4_data = np.asarray([[1, 2], [3, 4], [5, 6]]) * 0.01
        dataset["u_independent_Ch4"] = Variable(["y", "x"], u_ind_ch4_data)

        u_str_ch4_data = np.asarray([[7, 8], [9, 10], [11, 12]]) * 0.01
        dataset["u_structured_Ch4"] = Variable(["y", "x"], u_str_ch4_data)

        u_ind_ch5_data = np.asarray([[13, 14], [15, 16], [17, 18]]) * 0.01
        dataset["u_independent_Ch5"] = Variable(["y", "x"], u_ind_ch5_data)

        u_str_ch5_data = np.asarray([[14, 15], [16, 17], [18, 19]]) * 0.01
        dataset["u_structured_Ch5"] = Variable(["y", "x"], u_str_ch5_data)

        channels = ["Ch4", "Ch5", "satellite_zenith_angle"]

        disturbances = RadPropProcessor._calculate_radiance_disturbances(dataset, channels)
        self.assertEqual(2, len(disturbances))

        dist_data = disturbances["Ch4"]
        self.assertAlmostEqual(0.07071067811865477, dist_data[0, 0], 8)
        self.assertAlmostEqual(0.08246211251235322, dist_data[0, 1], 8)

        dist_data = disturbances["Ch5"]
        self.assertAlmostEqual(0.2193171219946131, dist_data[1, 0], 8)
        self.assertAlmostEqual(0.23345235059857505, dist_data[1, 1], 8)
