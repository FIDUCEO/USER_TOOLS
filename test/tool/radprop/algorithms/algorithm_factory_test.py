import unittest

from fiduceo.tool.radprop.algorithms.algorithm_factory import AlgorithmFactory
from fiduceo.tool.radprop.algorithms.avhrr_ndvi import AvhrrNDVI
from fiduceo.tool.radprop.algorithms.avhrr_simple_sst import AvhrrSimpleSST


class AlgorithmFactoryTest(unittest.TestCase):

    def test_get_names(self):
        factory = AlgorithmFactory()

        names = factory.get_names()
        self.assertEqual(3, len(names))
        self.assertTrue("AVHRR_SST_NAIVE" in names)
        self.assertTrue("AVHRR_SST_SIMPLE" in names)
        self.assertTrue("AVHRR_NDVI" in names)

    def test_get_algorithm(self):
        factory = AlgorithmFactory()

        algorithm = factory.get_algorithm("AVHRR_SST_SIMPLE")
        self.assertTrue(isinstance(algorithm, AvhrrSimpleSST))

        algorithm = factory.get_algorithm("AVHRR_NDVI")
        self.assertTrue(isinstance(algorithm, AvhrrNDVI))