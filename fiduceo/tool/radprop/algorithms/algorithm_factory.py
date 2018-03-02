from fiduceo.tool.radprop.algorithms.avhrr_naive_sst import AvhrrNaiveSST
from fiduceo.tool.radprop.algorithms.avhrr_ndvi import AvhrrNDVI
from fiduceo.tool.radprop.algorithms.avhrr_simple_sst import AvhrrSimpleSST


class AlgorithmFactory:

    def __init__(self):
        self.algorithms = dict([(AvhrrNaiveSST.get_name(), AvhrrNaiveSST()), (AvhrrSimpleSST.get_name(), AvhrrSimpleSST()), (AvhrrNDVI.get_name(), AvhrrNDVI())])

    def get_names(self):
        return ["AVHRR_SST_NAIVE", "AVHRR_SST_SIMPLE", "AVHRR_NDVI"]

    def get_algorithm(self, name):
        return self.algorithms[name]