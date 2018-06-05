import unittest

import numpy as np
import xarray as xr
from xarray import Variable

from fiduceo.tool.radprop.algorithms.mw_uth import MwUTH


class MwUTHTest(unittest.TestCase):

    def setUp(self):
        self.mw_uth = MwUTH()

    def test_get_name(self):
        self.assertEqual("MW_UTH", self.mw_uth.get_name())

    def test_get_variables_names(self):
        variable_names = self.mw_uth.get_variable_names()
        self.assertTrue("Ch3_BT" in variable_names)

    def test_process(self):
        dataset = xr.Dataset()

        ch4_data = np.asarray([[25668, 25741], [25708, 25684], [25709, 25753]]) * 0.01
        dataset["Ch3_BT"] = Variable(["y", "x"], ch4_data)

        result = self.mw_uth.process(dataset)

        self.assertIsNotNone(result)

        self.assertAlmostEqual(-1.5187, result.data[0, 1])
        self.assertAlmostEqual(-1.4956, result.data[1, 0])
        self.assertAlmostEqual(-1.5271, result.data[2, 1])
