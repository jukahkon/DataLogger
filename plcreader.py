"""
PLC READER
"""
import snap7.client as s7client
import snap7.util as s7util
#import sys
#sys.path.insert(1, './Mockup')
#import client as s7client
#import util as s7util
from snap7.snap7types import *
from pprint import pprint

plc_client = None

cache = {
    602 : { 'lenght': 490, 'data': b'' },
    660 : { 'lenght': 38, 'data': b'' },
    661 : { 'lenght': 38, 'data': b'' },
    662 : { 'lenght': 138, 'data': b'' },
    663 : { 'lenght': 52, 'data': b'' },
    664 : { 'lenght' : 8810, 'data' : b'' },
    665 : { 'lenght' : 8810, 'data' : b'' }
}

def connect():
    global plc_client

    plc_client = s7client.Client()
    plc_client.connect('10.0.0.3', 0, 1)

def disconnect():
    if plc_client:
        try:
            plc_client.disconnect()
        except:
            pass


def readTagValue(tag):
    area = tag['area']
    datatype = tag['datatype']
    db = tag['db']
    offset = tag['offset']
    size = tag['size']

    return readValue(area, db, datatype, offset, size )

def readValue(area, db, datatype, offset, size=0):
    if area == 'S7AreaDB' and db != 0:
        (buf, start) = readDataBlock(db, datatype, offset, size)
    elif area == 'S7AreaMK':
        (buf, start) = readMarker(datatype, offset, size)
    else:
        (buf, start) = (b'', 0)
    
    if buf:
        if datatype == 'INTEGER':
            value = s7util.get_int(buf, start)
        elif datatype == 'REAL':
            value = s7util.get_real(buf, start)
        elif datatype == 'STRING':
            value = s7util.get_string(buf, start, size)
        elif datatype == 'DATE_TIME':
            value = buf[:8]
        elif datatype == 'ARRAY OF REAL':
            value = []
            if len(buf) >= start + (4 * size):
                for i in range(0, size):
                    value.append(s7util.get_real(buf, start + (4 * i)))
    else:
        # print('setting default value')
        if datatype == 'INTEGER':
            value = 0
        elif datatype == 'REAL':
            value = 0.0
        elif datatype == 'STRING':
            value = ''
        elif datatype == 'DATE_TIME':
            value = b''
        elif datatype == 'ARRAY OF REAL':
            value = []
            for i in range(0, size):
                value.append(0.0)

    return value

def readDataBlock(db, datatype, offset, size):
    buf = b''

    if db in cache: 
        start = offset
        if not cache[db]['data']:
            buf = plc_client.read_area(S7AreaDB, db, 0, cache[db]['lenght'])
            cache[db]['data'] = buf
        else:
            buf = cache[db]['data']
    else:
        start = 0
        if datatype == 'INTEGER':
            buf = plc_client.read_area(S7AreaDB, db, offset, 2)
        elif datatype == 'REAL':
            buf = plc_client.read_area(S7AreaDB, db, offset, 4)
        elif datatype == 'STRING':
            buf = plc_client.read_area(S7AreaDB, db, offset, size)
        elif datatype == 'DATE_TIME':
            buf = plc_client.read_area(S7AreaDB, db, offset, 8)
        elif datatype == 'ARRAY OF REAL':
            buf = plc_client.read_area(S7AreaDB, db, offset, 4*size)
        else:
            print('Unsupported datatype for DB')

    return (buf, start)

def readMarker(datatype, offset, size):
    buf = ''

    if datatype == 'INTEGER':
        buf =  plc_client.read_area(S7AreaMK, 0, offset, 2)
    elif datatype == 'REAL':
        buf =  plc_client.read_area(S7AreaMK, 0, offset, 4)
    elif datatype == 'STRING':
        buf =  plc_client.read_area(S7AreaMK, 0, offset, size)
    else:
        print('Unsupported datatype for marker')

    return (buf, 0)

def clearCache():
    for key in cache:
        cache[key]['data'] = b''


if __name__ == "__main__":
    clearCache()
    connect()

    tag1 = { 'title' : 'Tyonumero', 'datatype' : 'INTEGER', 'area' : 'S7AreaDB', 'db' : 602, 'offset' : 0, 'size' : '' }
    tag2 = { 'title' : 'Aihion paino', 'datatype' : 'REAL', 'area' : 'S7AreaDB', 'db' : 602, 'offset' : 390, 'size' : '' }
    tag3 = { 'title' : 'Tilaaja', 'datatype' : 'STRING', 'area' : 'S7AreaDB', 'db' : 602, 'offset' : 136, 'size' : 20 }
    tag4 = { 'title' : 'Tilasana', 'datatype' : 'INTEGER', 'area' : 'S7AreaMK', 'db' : 0, 'offset' : 1008, 'size' : '' }
    tag5 = { 'title' : 'KUVA_NopeaEka', 'datatype' : 'REAL', 'area' : 'S7AreaDB', 'db' : 664, 'offset' : 10, 'size' : '' }
    tag6 = { 'title' : 'KUVA_NopeaVika', 'datatype' : 'REAL', 'area' : 'S7AreaDB', 'db' : 664, 'offset' : 8806, 'size' : '' }
    tag7 = { 'title' : 'DateTime', 'datatype' : 'DATE_TIME', 'area' : 'S7AreaDB', 'db' : 664, 'offset' : 0, 'size' : '' }
    tag8 = { 'title' : 'KYVA_Nopeat', 'datatype' : 'ARRAY OF REAL', 'area' : 'S7AreaDB', 'db' : 665, 'offset' : 0, 'size' : 4 }

    print("Tag 1 value: " +str(readTagValue(tag1)))
    print("Tag 2 value: " +str(readTagValue(tag2)))
    print("Tag 3 value: " +str(readTagValue(tag3)))
    print("Tag 4 value: " +str(readTagValue(tag4)))
    print("Tag 5 value: " +str(readTagValue(tag5)))
    print("Tag 6 value: " +str(readTagValue(tag6)))
    print("Tag 7 value: ")
    pprint(readTagValue(tag7)) # bytearray(b' \x03\x19\x08\x03\x05\x00\x05') 2020-03-19-08:03:05
    print("Tag 8 value: ")
    pprint(readTagValue(tag8))

    disconnect()
