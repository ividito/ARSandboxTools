import matplotlib.pyplot as plotter
from GridFileReader import readGridFile
from GridFileWriter import writeGridFile
from XYZFileReader import readXYZFile
import sys
import numpy as np
import pylab as plt
from scipy.interpolate import RegularGridInterpolator

# https://stackoverflow.com/questions/42275304/changing-data-resolution-in-python
def regrid(data, out_x, out_y):
    m = max(data.shape[0], data.shape[1])
    y = np.linspace(0, 1.0/m, data.shape[0])
    x = np.linspace(0, 1.0/m, data.shape[1])
    interpolating_function = RegularGridInterpolator((y, x), data)

    yv, xv = np.meshgrid(np.linspace(0, 1.0/m, out_y), np.linspace(0, 1.0/m, out_x))

    return interpolating_function((xv, yv))

def ConvertGridToXYZ(gridfile, xyzfile):
    rows, cols, left, bottom, right, top, griddata = readGridFile(gridfile)
    gridscale = cols/(right-left)  # scale of each datapoint in grid data (arbitrary units)
    xyzheader= 'x y z\n'
    xyzdata = []
    for y in range(rows):
        for x in range(cols):
            depth = griddata[y][x]+bottom
            lon = (x)+left
            lat = (y)  # no baseline in grid data for lat values, assume they begin at 0
            xyzdata.append((lon, lat, depth))
    # This xyz data is valid because: y value is determined by outer loop, x value is ascending in inner loop
    assert len(xyzdata) == rows*cols, "XYZ dimensions do not match grid size"
    with open(xyzfile,'w') as fout:
        fout.write(xyzheader)
        for data in xyzdata:
            fout.write("%f %f %f\n" % data)

def ConvertXYZToGrid(xyzfile, gridfile):
    readXYZFile(xyzfile)
    # These are constant
    rows = 480
    cols = 640
    xdata, ydata, zdata = readXYZFile(xyzfile)
    xdata = np.unique(xdata)
    ydata = np.unique(ydata)
    X, Y = np.meshgrid(xdata, ydata)
    Z = zdata.reshape(len(ydata), len(xdata))
    Z = regrid(Z, cols, rows)  # in case input resolution is not what we want
    Zmin = np.min(Z)
    Zmax = np.max(Z)
    Zmargin = (Zmax-Zmin)
    l = 0
    r = 0
    t = Zmax+Zmargin/2
    b = Zmin-Zmargin/2
    header = [rows, cols, l, b, r, t]
    writeGridFile(gridfile,Z, header)
    plotter.pcolormesh(X, Y, Z)
    plotter.show()
    return

if __name__ == "__main__":
    gridfile = sys.argv[1]
    xyzfile = sys.argv[2]
    mygridfile = 'myLakeTahoe.grid'
    ConvertGridToXYZ(gridfile, xyzfile)
    ConvertXYZToGrid(xyzfile, mygridfile)
    ConvertGridToXYZ(mygridfile, xyzfile)
    ConvertXYZToGrid(xyzfile, mygridfile)
