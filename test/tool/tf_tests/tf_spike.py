import unittest

import numpy as np
import tensorflow as tf

class TFTest(unittest.TestCase):

    def test_example_1(self):
        a = tf.constant(3.0, dtype=tf.float64)
        b = tf.constant(4.0, dtype=tf.float64)

        total = a + b

        session = tf.Session()
        print(session.run(total))

    def test_simpleOp_with_npArrays(self):
        ch4_data = np.asarray([[1089, 792], [1203, 223], [1203, 154]]) * 0.01
        ch5_data = np.asarray([[778, 569], [904, 92], [903, 40]]) * 0.01

        ch_4 = tf.Variable(ch4_data, dtype=tf.float32)
        ch_5 = tf.Variable(ch5_data, dtype=tf.float32)
        a = tf.constant(2.0, dtype=tf.float32)
        b = tf.constant(1.0, dtype=tf.float32)

        sst = a * ch_4 - ch_5 + b

        session = tf.Session()
        session.run(tf.global_variables_initializer())  # this one was not obvious!!!
        print(session.run(sst))


