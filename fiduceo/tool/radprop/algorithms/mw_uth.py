from numba import jit
from xarray import Variable


class MwUTH:

    @staticmethod
    def get_name():
        return "MW_UTH"

    def get_variable_names(self):
        return ["Ch3_BT"]

    def process(self, dataset):
        ch3_variable = dataset["Ch3_BT"]

        ln_uth = process_uth(ch3_variable.values)

        return Variable(ch3_variable.dims, ln_uth)


@jit('float64[:, :](float64[:, :])', nopython=True)
def process_uth(ch3_bt):
    return 16.5 + ch3_bt * (-0.07)