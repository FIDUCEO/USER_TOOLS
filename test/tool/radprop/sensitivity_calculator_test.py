import unittest

import numpy as np
import xarray as xr
from xarray import Variable

from fiduceo.tool.radprop.algorithms.avhrr_naive_sst import AvhrrNaiveSST
from fiduceo.tool.radprop.sensitivity_calculator import SensitivityCalculator


class SensitivityCalculatorTest(unittest.TestCase):

    def setUp(self):
        self.sensitivity_calculator = SensitivityCalculator()

    def test_calculate_two_variables(self):
        dataset = self._create_two_channel_dataset()
        disturbances = self._create_two_channel_disturbances()

        sensitivities = self.sensitivity_calculator.run(dataset, disturbances, AvhrrNaiveSST())

        self.assertEqual(2, len(sensitivities))
        ch4_sensitivity = sensitivities["Ch4"]
        self.assertAlmostEqual(0.8, ch4_sensitivity[0, 0], 8)
        self.assertAlmostEqual(0.78, ch4_sensitivity[0, 1], 8)
        self.assertAlmostEqual(0.82, ch4_sensitivity[1, 0], 8)

        ch5_sensitivity = sensitivities["Ch5"]
        self.assertAlmostEqual(-0.37, ch5_sensitivity[1, 1], 8)
        self.assertAlmostEqual(-0.42, ch5_sensitivity[2, 0], 8)
        self.assertAlmostEqual(-0.36, ch5_sensitivity[2, 1], 8)

    def test_create_subset(self):
        dataset = self._create_two_channel_dataset()

        ch6_data = np.asarray([[1090, 794], [1205, 225], [1205, 156]]) * 0.01
        dataset["Ch6"] = Variable(["y", "x"], ch6_data)

        ch7_data = np.asarray([[1090, 794], [1205, 225], [1205, 156]]) * 0.01
        dataset["Ch7"] = Variable(["y", "x"], ch7_data)

        subset = self.sensitivity_calculator._create_subset(dataset, {"Ch4", "Ch5"})
        self.assertIsNotNone(subset)
        self.assertTrue("Ch4" in subset.variables)
        self.assertTrue("Ch5" in subset.variables)
        self.assertFalse("Ch6" in subset.variables)
        self.assertFalse("Ch7" in subset.variables)

    def _create_two_channel_disturbances(self):
        ch4_data = np.asarray([[0.4, 0.39], [0.41, 0.38], [0.42, 0.37]])
        ch5_data = np.asarray([[0.39, 0.38], [0.4, 0.37], [0.42, 0.36]])
        disturbances = {"Ch4": ch4_data, "Ch5": ch5_data}
        return disturbances

    def _create_two_channel_dataset(self):
        dataset = xr.Dataset()
        ch4_data = np.asarray([[1090, 794], [1205, 225], [1205, 156]]) * 0.01
        dataset["Ch4"] = Variable(["y", "x"], ch4_data)
        ch5_data = np.asarray([[780, 571], [906, 94], [905, 42]]) * 0.01
        dataset["Ch5"] = Variable(["y", "x"], ch5_data)
        return dataset
