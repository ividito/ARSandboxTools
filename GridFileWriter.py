import struct
import sys

def writeFloatingPoint(flt):
    s = struct.pack('1f', flt)
    x = struct.unpack('f', s)[0]
    if len(s)<4:
        print repr(s)
    return s

def writeFloatingList(flt):
    s = struct.pack('f'*len(flt), *flt)
    #print s.encode('hex')
    return s

def writeLittleEndian(i):
    s = struct.pack('<i', i)
    return s

def writeGridFile(filename, data, headers):
    # data must be 2d array
    with open(filename, 'wb') as fout:
        for i in headers[:2]:
            fout.write(writeLittleEndian(i))
        for f in headers[2:]:
            fout.write(writeFloatingPoint(f))
        for row in data:
            for col in row:
                #if col>100:
                #    print col
                fout.write(writeFloatingPoint(col))

if __name__ == '__main__':
    x = [1.0,14.657,-87.4444, 2.22222]
    from GridFileReader import readFloatingPoint
    for d in x:
        print struct.unpack('f', (writeFloatingPoint(d)))[0]
