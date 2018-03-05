import os
from ConfigParser import ConfigParser


class TestDataUtils:
    __TEST_DATA_PATH = None

    @staticmethod
    def get_test_data_dir():
        global __TEST_DATA_PATH
        if TestDataUtils.__TEST_DATA_PATH is None:
            ini_file = os.path.join(os.path.dirname(__file__), "test_data.ini")
            if not os.path.isfile(ini_file):
                raise IOError("Missing configuration file: " + ini_file)

            parser = ConfigParser()
            parser.read(ini_file)
            __TEST_DATA_PATH = parser.get("TestData", "test_data_path")

        return __TEST_DATA_PATH
