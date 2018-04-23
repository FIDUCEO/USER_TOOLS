import os
import unittest

import numpy as np
import xarray as xr
from numba import jit

from test.tool.test_data_utils import TestDataUtils


class NumbaSpikeTest(unittest.TestCase):
    AVHRR_FCDR = "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1.nc"

    def setUp(self):
        self.target_file = None

        data_dir = TestDataUtils.get_test_data_dir()
        self.test_file = os.path.join(data_dir, self.AVHRR_FCDR)
        self.assertTrue(os.path.isfile(self.test_file))

    def test_the_test(self):
        dataset = xr.open_dataset(self.test_file, chunks=1024 * 1024)

        width = dataset.dims["x"]
        height = dataset.dims["y"]

        try:
            array = create_float_array(width, height)

            self.assertTrue(np.isnan(array[0, 0]))
        finally:
            dataset.close()


@jit('float32[:, :](int32, int32)')
#@jit(nopython=True)
def create_float_array(width, height):
    return np.full((height, width), np.NaN, dtype=np.float32).astype(np.float32)
