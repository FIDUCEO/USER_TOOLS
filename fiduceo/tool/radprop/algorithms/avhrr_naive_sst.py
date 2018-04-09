import tensorflow as tf
from xarray import Variable


class AvhrrNaiveSST:

    def __init__(self):
        self.ch_4 = tf.placeholder(dtype=tf.float64)
        self.ch_5 = tf.placeholder(dtype=tf.float64)

        a = tf.constant(2.0, dtype=tf.float64)
        b = tf.constant(1.0, dtype=tf.float64)

        self.sst = a * self.ch_4 - self.ch_5 + b

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())  # this one was not obvious!!!

    def process(self, dataset):
        ch4_variable = dataset["Ch4"]

        sst_data = self.session.run(self.sst, feed_dict={self.ch_4: dataset["Ch4"].data, self.ch_5: dataset["Ch5"].data})

        return Variable(ch4_variable.dims, sst_data)

    @staticmethod
    def get_name():
        return "AVHRR_SST_NAIVE"

    def get_variable_names(self):
        return ["Ch4", "Ch5"]
