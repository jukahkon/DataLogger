"""
PLC READER
"""
#import snap7.client
#import snap7.util
import Mockup.client as s7client
import Mockup.util as s7util
from snap7.snap7types import *

plc_client = None

cache = {
    # 602 : { 'lenght': 490, 'data': b'0' }
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
        buf = readDataBlock(db, datatype, offset, size)
    elif area == 'S7AreaMK':
        buf = readMarker(datatype, offset, size)
    else:
        buf = b''
    
    if buf:
        if datatype == 'INTEGER':
            value = s7util.get_int(buf, offset)
        elif datatype == 'REAL':
            value = s7util.get_real(buf, offset)
        elif datatype == 'STRING':
            value = s7util.get_string(buf, offset, size)

    return value

def readDataBlock(db, datatype, offset, size):
    buf = b''

    if db in cache: 
        if not cache[db]['data']:
            buf = plc_client.read_area(S7AreaDB, db, 0, cache[db]['lenght'])
            cache[db]['data'] = buf
        else:
            buf = cache[db]['data']
    else:
        if datatype == 'INTEGER':
            buf = plc_client.read_area(S7AreaDB, db, offset, 2)
        elif datatype == 'REAL':
            buf = plc_client.read_area(S7AreaDB, db, offset, 4)
        elif datatype == 'STRING':
            buf = plc_client.read_area(S7AreaDB, db, offset, size)

    return buf

def readMarker(datatype, offset, size):
    buf = ''

    if datatype == 'INTEGER':
        buf =  plc_client.read_area(S7AreaMK, 0, offset, 2)
    elif datatype == 'REAL':
        buf =  plc_client.read_area(S7AreaMK, 0, offset, 4)
    elif datatype == 'STRING':
        buf =  plc_client.read_area(S7AreaMK, 0, offset, size)

    return buf

def clearCache():
    for key in cache:
        cache[key] = b''


if __name__ == "__main__":
    clearCache()
    connect()

    tag1 = { 'title' : '', 'datatype' : 'INTEGER', 'area' : 'S7AreaDB', 'db' : 602, 'offset' : 0, 'size' : '' }
    tag2 = { 'title' : '', 'datatype' : 'REAL', 'area' : 'S7AreaDB', 'db' : 602, 'offset' : 2, 'size' : '' }
    tag3 = { 'title' : '', 'datatype' : 'STRING', 'area' : 'S7AreaDB', 'db' : 602, 'offset' : 6, 'size' : '20' }
    tag4 = { 'title' : '', 'datatype' : 'INTEGER', 'area' : 'S7AreaMK', 'db' : 0, 'offset' : 100, 'size' : '' }

    print("Tag 1 value: " +str(readTagValue(tag1)))
    print("Tag 2 value: " +str(readTagValue(tag2)))
    print("Tag 3 value: " +str(readTagValue(tag3)))
    print("Tag 4 value: " +str(readTagValue(tag4)))

    disconnect()
