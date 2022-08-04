import pandas
from Analyzer import fileName

x = pandas.read_pickle(fileName)
print(x)