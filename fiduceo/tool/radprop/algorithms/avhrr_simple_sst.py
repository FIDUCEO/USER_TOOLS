import numpy as np
from xarray import Variable
import tensorflow as tf


class AvhrrSimpleSST:

    def __init__(self):
        self.ch_4 = tf.placeholder(dtype=tf.float64)
        self.ch_5 = tf.placeholder(dtype=tf.float64)
        self.sza = tf.placeholder(dtype=tf.float64)

        b = tf.constant(1.0, dtype=tf.float64)
        to_rad = tf.constant(np.pi / 180.0, dtype=tf.float64)

        self.sst = self.ch_4 + b / tf.cos(self.sza * to_rad) * (self.ch_4 - self.ch_5) + b

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())  # this one was not obvious!!!

    def process(self, dataset):
        ch4_variable = dataset["Ch4"]

        sst_data = self.session.run(self.sst, feed_dict={self.ch_4: dataset["Ch4"].data, self.ch_5: dataset["Ch5"].data, self.sza: dataset["satellite_zenith_angle"].data})

        return Variable(ch4_variable.dims, sst_data)

    @staticmethod
    def get_name():
        return "AVHRR_SST_SIMPLE"

    def get_variable_names(self):
        return ["Ch4", "Ch5", "satellite_zenith_angle"]
