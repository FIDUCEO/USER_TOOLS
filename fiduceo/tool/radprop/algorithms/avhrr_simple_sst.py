import numpy as np
from numba import jit
from xarray import Variable


class AvhrrSimpleSST:

    def process(self, dataset):
        ch4_variable = dataset["Ch4"]

        sst_data = process_sst(dataset["Ch4"].values, dataset["Ch5"].values, dataset["satellite_zenith_angle"].values)

        return Variable(ch4_variable.dims, sst_data)

    @staticmethod
    def get_name():
        return "AVHRR_SST_SIMPLE"

    def get_variable_names(self):
        return ["Ch4", "Ch5", "satellite_zenith_angle"]


@jit('float64[:, :](float64[:, :], float64[:, :], float64[:, :])', nopython=True)
def process_sst(ch4, ch5, sza):
    return ch4 + 1.0 / np.cos(sza * np.pi / 180.0) * (ch4 - ch5) + 1.0
