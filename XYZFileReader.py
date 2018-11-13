import re
import numpy as np

def readXYZFile(xyzfile):
    data = open(xyzfile, 'r').readlines()
    header = data[0]
    if header[0] not in '-.0123456789':
        data = data[1:]
    p = re.compile(r'\d+\.\d+')  # Compile a pattern to capture float values
    data = [[float(i) for i in p.findall(s)] for s in data]  # Convert strings to float
    xdata = np.array([d[0] for d in data])
    ydata = np.array([d[1] for d in data])
    zdata = np.array([d[2] for d in data])
    return xdata, ydata, zdata