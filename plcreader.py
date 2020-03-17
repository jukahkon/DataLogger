"""
PLC READER
"""
import snap7.client as s7client
import snap7.util as s7util
""" import sys
sys.path.insert(1, './Mockup')
import client as s7client
import util as s7util """
from snap7.snap7types import *
from pprint import pprint

plc_client = None

cache = {
    602 : { 'lenght': 490, 'data': b'' }
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
    if area == 'S7AreaDB':
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
    else:
        print('setting default value')
        if datatype == 'INTEGER':
            value = 0
        elif datatype == 'REAL':
            value = 0.0
        elif datatype == 'STRING':
            value = ''

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
    tag3 = { 'title' : 'Tilaaja', 'datatype' : 'STRING', 'area' : 'S7AreaDB', 'db' : 602, 'offset' : 136, 'size' : '20' }
    tag4 = { 'title' : 'Tilasana', 'datatype' : 'INTEGER', 'area' : 'S7AreaMK', 'db' : 0, 'offset' : 1008, 'size' : '' }

    print("Tag 1 value: " +str(readTagValue(tag1)))
    print("Tag 2 value: " +str(readTagValue(tag2)))
    print("Tag 3 value: " +str(readTagValue(tag3)))
    print("Tag 4 value: " +str(readTagValue(tag4)))

    disconnect()
