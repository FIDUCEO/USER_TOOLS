import unittest

import numpy as np
import xarray as xr
from xarray import Variable

from fiduceo.tool.radprop.algorithms.avhrr_ndvi import AvhrrNDVI


class AvhrrNdviTest(unittest.TestCase):

    def testProcess(self):
        dataset = xr.Dataset()

        ch1_data = np.asarray([[1195, 1228], [902, 1747], [902, 1848]]) * 1e-4
        dataset["Ch1_Ref"] = Variable(["y", "x"], ch1_data)

        ch2_data = np.asarray([[886, 946], [608, 1514], [596, 1634]]) * 1e-4
        dataset["Ch2_Ref"] = Variable(["y", "x"], ch2_data)

        avhrr_ndvi = AvhrrNDVI()
        result = avhrr_ndvi.process(dataset)
        self.assertIsNotNone(result)

        self.assertAlmostEqual(-0.14848630466122062, result.data[0, 0])
        self.assertAlmostEqual(-0.071450475314320791, result.data[1, 1])
        self.assertAlmostEqual(-0.20427236315086786, result.data[2, 0])
