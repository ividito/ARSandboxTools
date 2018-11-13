import struct
import sys


def writeFloatingPoint(flt):
    s = struct.pack('f', flt)
    return s

def writeLittleEndian(i):
    s = struct.pack('<i', i)
    return s

def writeGridFile(filename, data, headers):
    # data must be 2d array
    with open(filename, 'w') as fout:
        for i in headers[:2]:
            fout.write(writeLittleEndian(i))
        for f in headers[2:]:
            fout.write(writeFloatingPoint(f))
        for row in data:
            for col in row:
                fout.write(writeFloatingPoint(col))

if __name__ == '__main__':
    x = [1.0,14.657,-87.4444]
    for d in x:
        print writeFloatingPoint(None, d)
