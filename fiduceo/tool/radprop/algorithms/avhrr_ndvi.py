import tensorflow as tf
from xarray import Variable


class AvhrrNDVI:

    def __init__(self):
        self.ch_1 = tf.placeholder(dtype=tf.float64)
        self.ch_2 = tf.placeholder(dtype=tf.float64)

        self.ndvi = (self.ch_2 - self.ch_1) / (self.ch_2 + self.ch_1)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())  # this one was not obvious!!!

    def process(self, dataset):
        ch1_variable = dataset["Ch1"]

        ndvi_data = self.session.run(self.ndvi, feed_dict={self.ch_1: dataset["Ch1"].data, self.ch_2: dataset["Ch2"].data})

        return Variable(ch1_variable.dims, ndvi_data)

    @staticmethod
    def get_name():
        return "AVHRR_NDVI"

    def get_variable_names(self):
        return ["Ch1", "Ch2"]
