import unittest

import numpy as np

from fiduceo.tool.radprop.error_covariances import ErrorCovariances


class ErrorCovariancesTest(unittest.TestCase):

    def test_calculate_2_2_uncorrelated(self):
        rci = np.asarray(([1.0, 0.0], [0.0, 1.0]), dtype=np.float64)
        ucv = np.asarray(([0.8, 0.6]), dtype=np.float64)

        error_covariances = ErrorCovariances()

        sci = error_covariances.calculate(ucv, rci)

        self.assertEqual((2, 2), sci.shape)
        self.assertAlmostEqual(0.64, sci[0, 0], 8)
        self.assertAlmostEqual(0.0, sci[1, 0], 8)
        self.assertAlmostEqual(0.0, sci[0, 1], 8)
        self.assertAlmostEqual(0.36, sci[1, 1], 8)

    def test_calculate_2_2_correlated(self):
        rci = np.asarray(([1.0, 0.24], [0.24, 1.0]), dtype=np.float64)
        ucv = np.asarray(([0.8, 0.6]), dtype=np.float64)

        error_covariances = ErrorCovariances()

        sci = error_covariances.calculate(ucv, rci)

        self.assertEqual((2, 2), sci.shape)
        self.assertAlmostEqual(0.64, sci[0, 0], 8)
        self.assertAlmostEqual(0.1152, sci[1, 0], 8)
        self.assertAlmostEqual(0.1152, sci[0, 1], 8)
        self.assertAlmostEqual(0.36, sci[1, 1], 8)

    def test_calculate_3_3_uncorrelated(self):
        rci = np.asarray(([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]), dtype=np.float64)
        ucv = np.asarray(([0.5, 0.4, 0.6]), dtype=np.float64)

        error_covariances = ErrorCovariances()

        sci = error_covariances.calculate(ucv, rci)

        self.assertEqual((3, 3), sci.shape)
        self.assertAlmostEqual(0.25, sci[0, 0], 8)
        self.assertAlmostEqual(0.0, sci[0, 1], 8)
        self.assertAlmostEqual(0.0, sci[0, 2], 8)
        self.assertAlmostEqual(0.0, sci[1, 0], 8)
        self.assertAlmostEqual(0.16, sci[1, 1], 8)
        self.assertAlmostEqual(0.0, sci[1, 2], 8)
        self.assertAlmostEqual(0.0, sci[2, 0], 8)
        self.assertAlmostEqual(0.0, sci[2, 1], 8)
        self.assertAlmostEqual(0.36, sci[2, 2], 8)

    def test_calculate_3_3_correlated(self):
        rci = np.asarray(([1.0, 0.2, 0.1], [0.2, 1.0, 0.2], [0.1, 0.2, 1.0]), dtype=np.float64)
        ucv = np.asarray(([0.5, 0.4, 0.6]), dtype=np.float64)

        error_covariances = ErrorCovariances()

        sci = error_covariances.calculate(ucv, rci)

        self.assertEqual((3, 3), sci.shape)
        self.assertAlmostEqual(0.25, sci[0, 0], 8)
        self.assertAlmostEqual(0.04, sci[0, 1], 8)
        self.assertAlmostEqual(0.03, sci[0, 2], 8)
        self.assertAlmostEqual(0.04, sci[1, 0], 8)
        self.assertAlmostEqual(0.16, sci[1, 1], 8)
        self.assertAlmostEqual(0.048, sci[1, 2], 8)
        self.assertAlmostEqual(0.03, sci[2, 0], 8)
        self.assertAlmostEqual(0.048, sci[2, 1], 8)
        self.assertAlmostEqual(0.36, sci[2, 2], 8)
