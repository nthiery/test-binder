import pandas
import numpy
from io import StringIO
from .ls_5 import line_source

class Model:
    def __init__(self, file=None, csv=None):
        if csv:
            assert file is None
            file = StringIO(csv)
        self.data = pandas.read_csv(file, sep=",", skiprows=[0])

    def __repr__(self):
        return "A XXX model with %s measures"%(len(self.normalized_temperature_series))

    @property
    def temperature_series(self):
        return self.data.set_index("t_s")['T']

    @property
    def normalized_temperature_series(self):
        t = self.temperature_series
        ti = t[:10]
        return t - ti.mean()

    def line_source(self, **kwargs):
        return line_source(tim=numpy.asarray(self.normalized_temperature_series.keys()), **kwargs)
