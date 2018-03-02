from xarray import Variable

class AvhrrNaiveSST:

    def process(self, dataset):
        ch4_variable = dataset["Ch4_Bt"]
        ch4_data = ch4_variable.data
        ch5_data = dataset["Ch5_Bt"].data

        sst = 2.0 * ch4_data - ch5_data + 1.0

        return Variable(ch4_variable.dims, sst)