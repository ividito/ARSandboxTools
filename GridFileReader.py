import struct
import sys


def readFloatingPoint(fileIn):
    x = fileIn.read(4)
    if len(x) < 4:
        print repr(x), fileIn.read(4).encode('hex'), fileIn.read(4).encode('hex')
    return struct.unpack('f', x)[0]

def readLittleEndian(fileIn):
    return struct.unpack('<i', fileIn.read(4))[0]

def readGridFile(gridfile):
    gridfile = sys.argv[1]
    fin = open(gridfile, 'rb')
    # The first 6 values are little-endian 4-byte numbers indicating grid size and geometric bounds
    x = tuple([readLittleEndian(fin) for _ in range(2)])
    cols, rows = x
    y = tuple([readFloatingPoint(fin) for _ in range(4)])
    leftedge, bottomedge, rightedge, topedge = y
    print x,y
    fulldata = []
    try:
        for r in range(rows):
            rowData = []
            for c in range(cols):
                rowData.append(readFloatingPoint(fin))
                # TODO the error check below doesnt work because bounds are signed and depth is unsigned (and relative?)
                # if min(rowData) < bottomedge or max(rowData) > topedge:
                #    raise Exception("Grid data exceeds grid bounds at row, column:", r, c)
            if len(rowData) != cols:
                raise Exception("Grid data is incomplete at row, column:", r, c)
            fulldata.append(rowData)
        if len(fulldata) != rows:
            raise Exception("Grid data is incomplete at row, column:", r, c)
    except Exception as e:
        print fulldata
        print e
        print fin.read(4).encode('hex')
    return rows, cols, leftedge, bottomedge, rightedge, topedge, fulldata

if __name__ == "__main__":
    filename = sys.argv[1]
    rows, cols, leftedge, bottomedge, rightedge, topedge, x = readGridFile(filename)
    print x[0]


