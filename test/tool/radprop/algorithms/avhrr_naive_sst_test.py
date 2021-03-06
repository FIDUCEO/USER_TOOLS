import unittest

import numpy as np
import xarray as xr
from xarray import Variable

from fiduceo.tool.radprop.algorithms.avhrr_naive_sst import AvhrrNaiveSST


class AvhrrNaiveSstTest(unittest.TestCase):

    def setUp(self):
        self.avhrr_sst = AvhrrNaiveSST()

    def test_process(self):
        dataset = xr.Dataset()

        ch4_data = np.asarray([[1089, 793], [1204, 224], [1204, 155]]) * 0.01
        dataset["Ch4"] = Variable(["y", "x"], ch4_data)

        ch5_data = np.asarray([[779, 570], [905, 93], [904, 41]]) * 0.01
        dataset["Ch5"] = Variable(["y", "x"], ch5_data)

        result = self.avhrr_sst.process(dataset)

        self.assertIsNotNone(result)
        self.assertAlmostEqual(11.16, result.data[0, 1])
        self.assertAlmostEqual(16.03, result.data[1, 0])
        self.assertAlmostEqual(3.6899999999999999, result.data[2, 1])

    def test_get_name(self):
        self.assertEqual("AVHRR_SST_NAIVE", self.avhrr_sst.get_name())

    def test_get_variables_names(self):
        variable_names = self.avhrr_sst.get_variable_names()
        self.assertTrue("Ch4" in variable_names)
        self.assertTrue("Ch5" in variable_names)
