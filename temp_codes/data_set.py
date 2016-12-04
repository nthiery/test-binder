import pandas
import numpy
from io import StringIO

class DataSet:
    def __init__(self, file=None, csv=None):
        if csv:
            assert file is None
            file = StringIO(csv)
        self.data = pandas.read_csv(file, sep=",", skiprows=[0])

    def __repr__(self):
        return "A XXX model with %s measures"%(len(self.temperature_responses))

    @property
    def temperatures(self):
        return self.data.set_index("t_s")['T']

    @property
    def times(self):
        #return self.data.iloc[10:]['t_s']
        return self.data.iloc[11:]['t_s']

    @property
    def temperature_responses(self):
        """
            >>> import sys
            >>> sys.path.append(".")
            >>> from temp_codes.data_set import DataSet
            >>> data_set = DataSet("temp_codes/agar_data_try.dat")
            >>> data_set.temperature_responses
            t_s
            0.0      0.002082
            0.5      0.003143
            ...
            179.5    0.481493
            180.0    0.489195
            Name: T, dtype: float64
        """
        t = self.temperatures
        ti = t.iloc[:10]
        # TODO: determine the first i such that t > 0
        #return t.iloc[10:] - ti.mean()
        return t.iloc[11:] - ti.mean()
