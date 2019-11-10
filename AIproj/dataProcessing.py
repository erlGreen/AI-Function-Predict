import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functions import *


class dataProcessing(object):
    def __init__(self, maxnr, filename):
        self.input = []
        self.output = []
        self.values = []
        if (filename == 0):
            for i in range(1, maxnr + 1):
                file = "./" + str(i) +".csv"
                self.values.extend(getData(file).tolist())
        else:
            self.values = getData(filename).tolist()
        self.macd = []
        self.signal = []

    def generateData(self, sequence):
        for i in range(0, len(self.values)):
            self.macd.append(MACD(self.values, i))
            self.signal.append(SIGNAL(self.macd, i))
        self.normalizeValue = max(map(abs, self.values))
        self.normalizeMACD = max(map(abs, self.macd))
        self.normalizeSignal = max(map(abs, self.signal))
        self.values[:] = [x / self.normalizeValue for x in self.values]
        self.macd[:] = [x / max(self.normalizeSignal, self.normalizeMACD) for x in self.macd]
        self.signal[:] = [x / max(self.normalizeSignal, self.normalizeMACD) for x in self.signal]
        for i in range(0, len(self.values) - sequence - 1):
            x = self.values[i: i + sequence]
            x.extend(self.macd[i: i + sequence])
            x.extend(self.signal[i: i + sequence])
            y = [self.values[i + sequence + 1]]
            self.input.append(x)
            self.output.append(y)
        self.input = np.array(self.input)
        self.output = np.array(self.output)