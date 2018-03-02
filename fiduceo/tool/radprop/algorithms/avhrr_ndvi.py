from xarray import Variable


class AvhrrNDVI:

    def process(self, dataset):
        ch1_variable = dataset["Ch1_Ref"]
        ch1_data = ch1_variable.data
        ch2_data = dataset["Ch2_Ref"].data

        ndvi = (ch2_data - ch1_data) / (ch2_data + ch1_data)

        return Variable(ch1_variable.dims, ndvi)

    @staticmethod
    def get_name():
        return "AVHRR_NDVI"
