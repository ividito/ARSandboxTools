import matplotlib.pyplot as plotter
from GridFileReader import readGridFile
from GridFileWriter import writeGridFile
from XYZFileReader import readXYZFile
import sys
import matplotlib.tri as tri
import numpy as np
import pylab as plt
from scipy.interpolate import griddata
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
    xyzheader= 'x y z\n'
    xyzdata = []
    for y in range(rows):
        for x in range(cols):
            depth = griddata[y][x]  # +bottom
            #if abs(depth)>2000:
                #print griddata[y][x], y, x, bottom
                #print ""
            lon = (x)+left
            lat = (y)+bottom
            xyzdata.append((lon, lat, depth))
    # This xyz data is valid because: y value is determined by outer loop, x value is ascending in inner loop
    assert len(xyzdata) == rows*cols, "XYZ dimensions do not match grid size"
    with open(xyzfile,'w') as fout:
        fout.write(xyzheader)
        for data in xyzdata:
            d1, d2, d3 = data
            #if abs(d3)>1000:
            #    print data
            fout.write("%f %f %f\n" % (d1,d2,d3))

def ConvertXYZToGrid(xyzfile, gridfile):
    #readXYZFile(xyzfile)
    # These are constant
    rows = 480
    cols = 640
    xdata, ydata, zdata = readXYZFile(xyzfile)
    xi = np.linspace(np.min(xdata), np.max(xdata), cols)
    yi = np.linspace(np.min(ydata), np.max(ydata), rows)
    Z = griddata((xdata, ydata), zdata, (xi[None, :], yi[:, None]), method='nearest')
    Zmin = np.min(Z)
    Zmax = np.max(Z)
    l = np.min(xdata)
    r = np.max(xdata)
    t = np.max(ydata)
    b = np.min(ydata)
    print l,r,b,t
    header = [cols, rows, l, b, r, t]
    writeGridFile(gridfile, Z, header)
    plotter.pcolormesh(xi, yi, Z)
    plotter.show()
    print Zmax, Zmin
    return

if __name__ == "__main__":
    gridfile = sys.argv[1]
    xyzfile = sys.argv[2]
    ConvertXYZToGrid(xyzfile, gridfile) #writes bad values (for no reason???)
    ConvertGridToXYZ(gridfile, 'target.xyz') #reads bad values
    ConvertXYZToGrid('target.xyz', 'newtarget.grid')
