import numpy as np
from xarray import Variable


class AvhrrSimpleSST:

    def process(self, dataset):
        ch4_variable = dataset["Ch4_Bt"]
        ch4_data = ch4_variable.data
        ch5_data = dataset["Ch5_Bt"].data
        sza_data = dataset["satellite_zenith_angle"].data

        sst = ch4_data + 1.0 / np.cos(sza_data) * (ch4_data - ch5_data) + 1.0

        return Variable(ch4_variable.dims, sst)

    @staticmethod
    def get_name():
        return "AVHRR_SST_SIMPLE"
