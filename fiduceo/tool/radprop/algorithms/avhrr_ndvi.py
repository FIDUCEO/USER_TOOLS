from numba import jit
from xarray import Variable


class AvhrrNDVI:

    def process(self, dataset):
        ch1_variable = dataset["Ch1"]

        ndvi_data = process_ndvi(dataset["Ch1"].values, dataset["Ch2"].values)

        return Variable(ch1_variable.dims, ndvi_data)

    @staticmethod
    def get_name():
        return "AVHRR_NDVI"

    def get_variable_names(self):
        return ["Ch1", "Ch2"]


@jit('float64[:, :](float64[:, :], float64[:, :])', nopython=True, parallel=True)
def process_ndvi(ch1, ch2):
    return (ch2 - ch1) / (ch2 + ch1)
