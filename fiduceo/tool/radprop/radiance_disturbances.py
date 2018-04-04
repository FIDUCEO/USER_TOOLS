import numpy as np
import tensorflow as tf


class RadianceDisturbances:

    def __init__(self):
        self.u_ind = tf.placeholder(dtype=tf.float64)
        self.u_str = tf.placeholder(dtype=tf.float64)
        self.u_com = tf.placeholder(dtype=tf.float64)
        self.rad_delta_tf = tf.sqrt(self.u_ind * self.u_ind + self.u_str * self.u_str + self.u_com * self.u_com)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())  # this one was not obvious!!!

    def calculate(self, dataset, variable_names):
        disturbances = dict()

        y = dataset.dims["y"]
        x = dataset.dims["x"]
        for variable_name in variable_names:
            u_ind_name = "u_independent_" + variable_name

            u_ind_data = None
            if u_ind_name in dataset:
                u_ind_data = dataset[u_ind_name].data

            u_str_name = "u_structured_" + variable_name
            u_str_data = None
            if u_str_name in dataset:
                u_str_data = dataset[u_str_name].data

            u_com_name = "u_common_" + variable_name
            u_com_data = None
            if u_com_name in dataset:
                u_com_data = dataset[u_com_name].data

            if u_str_data is None and u_ind_data is None and u_com_data is None:
                continue  # if no uncertainty can be found we skip this variable from calculation tb 2018-04-04

            if u_ind_data is None:
                u_ind_data = np.zeros([y, x])

            if u_str_data is None:
                u_str_data = np.zeros([y, x])

            if u_com_data is None:
                u_com_data = np.zeros([y, x])

            rad_delta = self.session.run(self.rad_delta_tf, feed_dict={self.u_str: u_str_data, self.u_ind: u_ind_data, self.u_com: u_com_data})
            disturbances.update({variable_name: rad_delta})

        return disturbances
