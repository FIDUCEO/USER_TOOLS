from numba import jit
from xarray import Variable


class AvhrrNaiveSST:

    def process(self, dataset):
        ch4_variable = dataset["Ch4"]

        sst_data = process_sst(dataset["Ch4"].values, dataset["Ch5"].values)

        return Variable(ch4_variable.dims, sst_data)

    @staticmethod
    def get_name():
        return "AVHRR_SST_NAIVE"

    def get_variable_names(self):
        return ["Ch4", "Ch5"]


@jit('float64[:, :](float64[:, :], float64[:, :])', nopython=True, parallel=True)
def process_sst(ch4, ch5):
    return 2.0 * ch4 - ch5 + 1.0
