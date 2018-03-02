import unittest

import numpy as np
import xarray as xr
from xarray import Variable

from fiduceo.tool.radprop.algorithms.avhrr_simple_sst import AvhrrSimpleSST


class AvhrrSimpleSstTest(unittest.TestCase):

    def testProcess(self):
        dataset = xr.Dataset()

        ch4_data = np.asarray([[1089, 793], [1204, 224], [1204, 155]]) * 0.01
        dataset["Ch4_Bt"] = Variable(["y", "x"], ch4_data)

        ch5_data = np.asarray([[779, 570], [905, 93], [904, 41]]) * 0.01
        dataset["Ch5_Bt"] = Variable(["y", "x"], ch5_data)

        sat_za_data = np.asarray([[6871, 6825], [6871, 6825], [6871, 6825]]) * 0.01
        dataset["satellite_zenith_angle"] = Variable(["y", "x"], sat_za_data)

        avhrr_sst = AvhrrSimpleSST()
        result = avhrr_sst.process(dataset)

        self.assertIsNotNone(result)

        self.assertAlmostEqual(12.36811672342432, result.data[0, 1])
        self.assertAlmostEqual(16.293227504189915, result.data[1, 0])
        self.assertAlmostEqual(4.307602271167589, result.data[2, 1])
