import unittest

import numpy as np

from fiduceo.tool.radprop.rad_prop_processor import RadPropProcessor, calculate_covariances, calculate_uncertainty


class RadPropProcessorTest(unittest.TestCase):

    def test_create_target_file_name(self):
        target_file_name = RadPropProcessor._create_target_filename("FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1.nc", "AVHRR_SST_NAIVE")
        self.assertEqual("FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1_AVHRR_SST_NAIVE.nc", target_file_name)

    def test_get_algorithm_help_strings(self):
        processor = RadPropProcessor()

        help_string = processor.get_algorithm_help_string()
        self.assertEqual("available algorithms are:\n" + "- AVHRR_SST_NAIVE\n" + "- AVHRR_SST_SIMPLE\n" + "- AVHRR_NDVI\n", help_string)

    def test_calculate_covariances_2vars_uncorrelated(self):
        correlation_matrix =  np.diag(np.ones(2, dtype=np.float64))
        uncertainty_vector = np.array([0.72, 0.56], dtype=np.float64)

        covariances = calculate_covariances(uncertainty_vector, correlation_matrix)
        self.assertEqual((2, 2), covariances.shape)
        self.assertAlmostEqual(0.5184, covariances[0, 0], 8)
        self.assertAlmostEqual(0.0, covariances[0, 1], 8)
        self.assertAlmostEqual(0.0, covariances[1, 0], 8)
        self.assertAlmostEqual(0.3136, covariances[1, 1], 8)

    def test_calculate_covariances_2vars_correlated(self):
        correlation_matrix =  np.diag(np.ones(2, dtype=np.float64))
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
        correlation_matrix =  np.diag(np.ones(3, dtype=np.float64))
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
        correlation_matrix =  np.diag(np.ones(3, dtype=np.float64))
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
