from fiduceo.tool.radprop.algorithms.avhrr_naive_sst import AvhrrNaiveSST
from fiduceo.tool.radprop.algorithms.avhrr_ndvi import AvhrrNDVI
from fiduceo.tool.radprop.algorithms.avhrr_simple_sst import AvhrrSimpleSST
from fiduceo.tool.radprop.algorithms.mw_uth import MwUTH


class AlgorithmFactory:

    def __init__(self):
        self.algorithms = dict([(AvhrrNaiveSST.get_name(), AvhrrNaiveSST()),
                                (AvhrrSimpleSST.get_name(), AvhrrSimpleSST()),
                                (AvhrrNDVI.get_name(), AvhrrNDVI()),
                                (MwUTH.get_name(), MwUTH())])

    def get_names(self):
        return self.algorithms.keys()

    def get_algorithm(self, name):
        return self.algorithms[name]
