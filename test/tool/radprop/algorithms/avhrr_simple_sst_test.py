import unittest

import numpy as np
import xarray as xr
from xarray import Variable

from fiduceo.tool.radprop.algorithms.avhrr_simple_sst import AvhrrSimpleSST


class AvhrrSimpleSstTest(unittest.TestCase):

    def setUp(self):
        self.avhrr_sst = AvhrrSimpleSST()

    def test_process(self):
        dataset = xr.Dataset()

        ch4_data = np.asarray([[1089, 793], [1204, 224], [1204, 155]]) * 0.01
        dataset["Ch4"] = Variable(["y", "x"], ch4_data)

        ch5_data = np.asarray([[779, 570], [905, 93], [904, 41]]) * 0.01
        dataset["Ch5"] = Variable(["y", "x"], ch5_data)

        sat_za_data = np.asarray([[6871, 6825], [6871, 6825], [6871, 6825]]) * 0.01
        dataset["satellite_zenith_angle"] = Variable(["y", "x"], sat_za_data)

        result = self.avhrr_sst.process(dataset)

        self.assertIsNotNone(result)

        self.assertAlmostEqual(14.94796044085826, result.data[0, 1])
        self.assertAlmostEqual(21.274904327787702, result.data[1, 0])
        self.assertAlmostEqual(5.6264461446539977, result.data[2, 1])

    def test_get_name(self):
        self.assertEqual("AVHRR_SST_SIMPLE", self.avhrr_sst.get_name())

    def test_get_variables_names(self):
        variable_names = self.avhrr_sst.get_variable_names()
        self.assertTrue("Ch4" in variable_names)
        self.assertTrue("Ch5" in variable_names)
        self.assertTrue("satellite_zenith_angle" in variable_names)
