import unittest

import numpy as np
import xarray as xr
from xarray import Variable

from fiduceo.tool.radprop.rad_prop_processor import RadPropProcessor, calculate_covariances, calculate_uncertainty, calculate_total_uncertainty, create_float_array, create_float_array_3D


class RadPropProcessorTest(unittest.TestCase):

    def test_create_target_file_name(self):
        target_file_name = RadPropProcessor._create_target_filename("FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1.nc", "AVHRR_SST_NAIVE")
        self.assertEqual("FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_SST_NAIVE.nc", target_file_name)

    def test_get_algorithm_help_strings(self):
        processor = RadPropProcessor()

        help_string = processor.get_algorithm_help_string()
        self.assertEqual("available algorithms are:\n" + "- AVHRR_SST_NAIVE\n" + "- AVHRR_SST_SIMPLE\n" + "- AVHRR_NDVI\n" + "- MW_UTH\n", help_string)

    def test_calculate_covariances_2vars_uncorrelated(self):
        correlation_matrix = np.diag(np.ones(2, dtype=np.float64))
        uncertainty_vector = np.array([0.72, 0.56], dtype=np.float64)

        covariances = calculate_covariances(uncertainty_vector, correlation_matrix)
        self.assertEqual((2, 2), covariances.shape)
        self.assertAlmostEqual(0.5184, covariances[0, 0], 8)
        self.assertAlmostEqual(0.0, covariances[0, 1], 8)
        self.assertAlmostEqual(0.0, covariances[1, 0], 8)
        self.assertAlmostEqual(0.3136, covariances[1, 1], 8)

    def test_calculate_covariances_2vars_correlated(self):
        correlation_matrix = np.diag(np.ones(2, dtype=np.float64))
        correlation_matrix[0, 1] = 0.27
        correlation_matrix[1, 0] = 0.27
        uncertainty_vector = np.array([0.72, 0.56], dtype=np.float64)

        covariances = calculate_covariances(uncertainty_vector, correlation_matrix)
        self.assertEqual((2, 2), covariances.shape)
        self.assertAlmostEqual(0.5184, covariances[0, 0], 8)
        self.assertAlmostEqual(0.108864, covariances[0, 1], 8)
        self.assertAlmostEqual(0.108864, covariances[1, 0], 8)
        self.assertAlmostEqual(0.3136, covariances[1, 1], 8)

    def test_calculate_covariances_3vars_uncorrelated(self):
        correlation_matrix = np.diag(np.ones(3, dtype=np.float64))
        uncertainty_vector = np.array([0.96, 0.63, 0.27], dtype=np.float64)

        covariances = calculate_covariances(uncertainty_vector, correlation_matrix)
        self.assertEqual((3, 3), covariances.shape)
        self.assertAlmostEqual(0.9216, covariances[0, 0], 8)
        self.assertAlmostEqual(0.0, covariances[0, 1], 8)
        self.assertAlmostEqual(0.0, covariances[0, 2], 8)
        self.assertAlmostEqual(0.0, covariances[1, 0], 8)
        self.assertAlmostEqual(0.3969, covariances[1, 1], 8)
        self.assertAlmostEqual(0.0, covariances[1, 2], 8)
        self.assertAlmostEqual(0.0, covariances[2, 0], 8)
        self.assertAlmostEqual(0.0, covariances[2, 1], 8)
        self.assertAlmostEqual(0.0729, covariances[2, 2], 8)

    def test_calculate_covariances_3vars_partially_correlated(self):
        correlation_matrix = np.diag(np.ones(3, dtype=np.float64))
        correlation_matrix[1, 2] = 0.4
        correlation_matrix[2, 1] = 0.4
        uncertainty_vector = np.array([0.96, 0.63, 0.27], dtype=np.float64)

        covariances = calculate_covariances(uncertainty_vector, correlation_matrix)
        self.assertEqual((3, 3), covariances.shape)
        self.assertAlmostEqual(0.9216, covariances[0, 0], 8)
        self.assertAlmostEqual(0.0, covariances[0, 1], 8)
        self.assertAlmostEqual(0.0, covariances[0, 2], 8)
        self.assertAlmostEqual(0.0, covariances[1, 0], 8)
        self.assertAlmostEqual(0.3969, covariances[1, 1], 8)
        self.assertAlmostEqual(0.06804, covariances[1, 2], 8)
        self.assertAlmostEqual(0.0, covariances[2, 0], 8)
        self.assertAlmostEqual(0.06804, covariances[2, 1], 8)
        self.assertAlmostEqual(0.0729, covariances[2, 2], 8)

    def test_calculate_uncertainty_2channel_uncorrelated(self):
        uncertainty_px = np.array([0.34, 0.076], dtype=np.float64)
        covariance = np.array([[0.978, 0.0], [0.0, 0.965]], dtype=np.float64)

        uncertainty = calculate_uncertainty(uncertainty_px, covariance)
        self.assertAlmostEqual(0.34442800283432007, uncertainty, 7)

    def test_calculate_uncertainty_2channel_correlated(self):
        uncertainty_px = np.array([0.34, 0.076], dtype=np.float64)
        covariance = np.array([[0.978, 0.034], [0.034, 0.965]], dtype=np.float64)

        uncertainty = calculate_uncertainty(uncertainty_px, covariance)
        self.assertAlmostEqual(0.3469693958759308, uncertainty, 8)

    def test_calculate_uncertainty_3channel_uncorrelated(self):
        uncertainty_px = np.array([0.34, 0.076, 0.52], dtype=np.float64)
        covariance = np.array([[0.978, 0.0, 0.0], [0.0, 0.621, 0.0], [0.0, 0.0, 0.965]], dtype=np.float64)

        uncertainty = calculate_uncertainty(uncertainty_px, covariance)
        self.assertAlmostEqual(0.6144751310348511, uncertainty, 7)

    def test_calculate_uncertainty_3channel_correlated(self):
        uncertainty_px = np.array([0.34, 0.076, 0.52], dtype=np.float64)
        covariance = np.array([[0.978, 0.1, 0.1], [0.1, 0.621, 0.1], [0.1, 0.1, 0.965]], dtype=np.float64)

        uncertainty = calculate_uncertainty(uncertainty_px, covariance)
        self.assertAlmostEqual(0.6526957154273987, uncertainty, 8)

    def test_calculate_total_uncertainty_2channel_uncorrelated(self):
        uncertainty_px = np.array([0.34, 0.076], dtype=np.float64)
        cov_i = np.array([[0.978, 0.0], [0.0, 0.965]], dtype=np.float64)
        cov_s = np.array([[0.235, 0.0], [0.0, 0.567]], dtype=np.float64)

        uncertainty = calculate_total_uncertainty(uncertainty_px, cov_i, cov_s)
        self.assertAlmostEqual(0.3860979676246643, uncertainty, 7)

    def test_calculate_total_uncertainty_3channel_correlated(self):
        uncertainty_px = np.array([0.34, 0.076, 0.208], dtype=np.float64)
        cov_i = np.array([[0.978, 0.1, 0.1], [0.1, 0.895, 0.1], [0.1, 0.1, 0.965]], dtype=np.float64)
        cov_s = np.array([[0.235, 0.1, 0.1], [0.1, 0.567, 0.1], [0.1, 0.1, 0.884]], dtype=np.float64)

        uncertainty = calculate_total_uncertainty(uncertainty_px, cov_i, cov_s)
        self.assertAlmostEqual(0.5230770707130432, uncertainty, 7)

    def test_create_float_array(self):
        float_array = create_float_array(21, 76)

        self.assertEqual((76, 21), float_array.shape)
        self.assertEqual(np.float32, float_array.dtype)
        self.assertAlmostEqual(0.0, float_array[56, 11], 8)

    def test_create_float_array_3d(self):
        float_array = create_float_array_3D(15, 54, 4)

        self.assertEqual((4, 54, 15), float_array.shape)
        self.assertEqual(np.float32, float_array.dtype)
        self.assertAlmostEqual(0.0, float_array[1, 46, 12], 8)

    def test_extract_channel_indices(self):
        channel_names = ["Ch4", "Ch5"]

        channel_indices = RadPropProcessor._extract_channel_indices(None, channel_names)
        self.assertEqual(2, len(channel_indices))
        self.assertEqual(4, channel_indices["Ch4"])
        self.assertEqual(5, channel_indices["Ch5"])

        channel_names = ["Ch2_BT", "Ch4_BT"]

        channel_indices = RadPropProcessor._extract_channel_indices(None, channel_names)
        self.assertEqual(2, len(channel_indices))
        self.assertEqual(1, channel_indices["Ch2_BT"])
        self.assertEqual(3, channel_indices["Ch4_BT"])

    def test_subset_correlation_matrices_none_available(self):
        dataset = xr.Dataset()
        channel_indices =  dict([("ch_1", 0), ("ch_3", 2)])

        rci, rcs, rcu = RadPropProcessor._subset_correlation_matrices(dataset, channel_indices)
        self.assertEqual((2, 2), rci.shape)
        self.assertAlmostEqual(1.0, rci[0, 0], 8)
        self.assertAlmostEqual(0.0, rci[1, 0], 8)

        self.assertEqual((2, 2), rcs.shape)
        self.assertAlmostEqual(0.0, rcs[0, 1], 8)
        self.assertAlmostEqual(1.0, rcs[1, 1], 8)

        self.assertEqual((2, 2), rcu.shape)
        self.assertAlmostEqual(1.0, rcu[0, 0], 8)
        self.assertAlmostEqual(0.0, rcu[1, 0], 8)

    def test_subset_correlation_matrices(self):
        dataset = xr.Dataset()

        u_cor_common = np.array([[1.0, 0.52, 0.46, 0.49], [0.52, 1.0, 0.82, 0.87], [0.46, 0.82, 1.0, 0.85], [0.49, 0.87, 0.85, 1.0]], dtype=np.float64)
        dataset["channel_correlation_matrix_common"] = Variable(["channel", "channel"], u_cor_common)

        u_cor_indep = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]], dtype=np.float64)
        dataset["channel_correlation_matrix_independent"] = Variable(["channel", "channel"], u_cor_indep)

        u_cor_struc = np.array([[1.0, 0.1, 0.09, 0.12], [0.1, 1.0, 0.06, 0.07], [0.09, 0.06, 1.0, 0.07], [0.12, 0.07, 0.07, 1.0]], dtype=np.float64)
        dataset["channel_correlation_matrix_structured"] = Variable(["channel", "channel"], u_cor_struc)

        channel_indices = dict([("ch_1", 0), ("ch_3", 2)])

        rci, rcs, rcu = RadPropProcessor._subset_correlation_matrices(dataset, channel_indices)

        self.assertEqual((2, 2), rci.shape)
        self.assertAlmostEqual(1.0, rci[0, 0], 8)
        self.assertAlmostEqual(0.0, rci[1, 0], 8)

        self.assertEqual((2, 2), rcs.shape)
        self.assertAlmostEqual(0.09, rcs[0, 1], 8)
        self.assertAlmostEqual(1.0, rcs[1, 1], 8)

        self.assertEqual((2, 2), rcu.shape)
        self.assertAlmostEqual(1.0, rcu[0, 0], 8)
        self.assertAlmostEqual(0.46, rcu[1, 0], 8)
