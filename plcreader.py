"""
PLC READER
"""
import snap7.client
import snap7.util
from snap7.snap7types import *

cache = {
    "DB602" : b'0'
}

def init():
    # connect
    pass

def connect():
    pass

def disconnect():
    pass

def readReal(db, offset):
    pass

def readInt(db, offset):
    pass

def readString(db, offset, lenght):
    pass

def cleanup():
    for key in cache:
        cache[key] = b''


    pass


