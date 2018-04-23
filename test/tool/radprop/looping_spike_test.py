import os
import unittest

import tensorflow as tf

from test.tool.test_data_utils import TestDataUtils


def condition(x, y, width, height):
    return tf.logical_and(tf.less(x, width), tf.less(y, height))


def body(x, y, width, height):
    x += 1
    x, y = tf.cond(tf.greater_equal(x, width), lambda: increment_y(x, y), lambda: don_t(x, y))

    return x, y, width, height


def increment_y(x, y):
    x = 0
    y += 1
    return x, y


def don_t(x, y):
    return x, y


class LoopingSpikeTest(unittest.TestCase):
    AVHRR_FCDR = "FIDUCEO_FCDR_L1C_AVHRR_NOAA11_19920704103249_19920704121448_EASY_v0.4pre_fv1.1.1.nc"

    def setUp(self):
        self.target_file = None

        data_dir = TestDataUtils.get_test_data_dir()
        self.test_file = os.path.join(data_dir, self.AVHRR_FCDR)
        self.assertTrue(os.path.isfile(self.test_file))

    # def test_run_a_tf_loop(self):  #     dataset = xr.open_dataset(self.test_file, chunks=1024 * 1024)  #  #     width = dataset.dims["x"]  #     height = dataset.dims["y"]  #  #     ch4_variable = dataset["Ch4"]  #  #     for y in range(0,height):  #         for x in range(0, width):  #             pass

    # tf_width = tf.constant(width)  # tf_height = tf.constant(height)  # result = tf.while_loop(condition, body, [0, 0, tf_width, tf_height], parallel_iterations=8)  #  # session = tf.Session()  # session.run(tf.global_variables_initializer())  # session.run(result)

    # dataset.close()
