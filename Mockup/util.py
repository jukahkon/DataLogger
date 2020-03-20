
try:
    # try with the standard library
    from collections import OrderedDict
except ImportError:
    # fallback to Python 2.6-2.4 back-port
    from ordereddict import OrderedDict


import struct
import logging
from snap7 import six
import re

logger = logging.getLogger(__name__)

def get_bool(_bytearray, byte_index, bool_index):
    return True


def set_bool(_bytearray, byte_index, bool_index, value):
    """
    Set boolean value on location in bytearray
    """
    assert value in [0, 1, True, False]
    # current_value = get_bool(_bytearray, byte_index, bool_index)
    index_value = 1 << bool_index

    if value:
        # make sure index_v is IN current byte
        _bytearray[byte_index] += index_value
    else:
        # make sure index_v is NOT in current byte
        _bytearray[byte_index] -= index_value


def set_int(bytearray_, byte_index, _int):
    """
    Set value in bytearray to int
    """
    # make sure were dealing with an int
    _int = int(_int)
    _bytes = struct.unpack('2B', struct.pack('>h', _int))
    bytearray_[byte_index:byte_index + 2] = _bytes
    return bytearray_


def get_int(bytearray_, byte_index):
    """
    Get int value from bytearray.

    int are represented in two bytes
    """
    """ data = bytearray_[byte_index:byte_index + 2]
    data[1] = data[1] & 0xff
    data[0] = data[0] & 0xff
    packed = struct.pack('2B', *data)
    value = struct.unpack('>h', packed)[0]
    return value """
    return int(1)


def set_real(_bytearray, byte_index, real):
    """
    Set Real value

    make 4 byte data from real

    """
    real = float(real)
    real = struct.pack('>f', real)
    _bytes = struct.unpack('4B', real)
    for i, b in enumerate(_bytes):
        _bytearray[byte_index + i] = b


def get_real(_bytearray, byte_index):
    """
    Get real value. create float from 4 bytes
    """
    if len(_bytearray) >= 4:
        x = _bytearray[byte_index:byte_index + 4]
        real = struct.unpack('>f', x)[0]
        return real
    else:
        return float(1.2)


def set_string(_bytearray, byte_index, value, max_size):
    """
    Set string value

    :params value: string data
    :params max_size: max possible string size
    """
    if six.PY2:
        assert isinstance(value, (str, unicode))
    else:
        assert isinstance(value, str)

    size = len(value)
    # FAIL HARD WHEN trying to write too much data into PLC
    if size > max_size:
        raise ValueError('size %s > max_size %s %s' % (size, max_size, value))
    # set len count on first position
    _bytearray[byte_index + 1] = len(value)

    i = 0
    # fill array which chr integers
    for i, c in enumerate(value):
        _bytearray[byte_index + 2 + i] = ord(c)

    # fill the rest with empty space
    for r in range(i + 1, _bytearray[byte_index]):
        _bytearray[byte_index + 2 + r] = ord(' ')


def get_string(_bytearray, byte_index, max_size):
    """
    parse string from bytearray
    """
    """ size = _bytearray[byte_index + 1]

    if max_size < size:
        logger.error("the string is to big for the size encountered in specification")
        logger.error("WRONG SIZED STRING ENCOUNTERED")
        size = max_size

    data = map(chr, _bytearray[byte_index + 2:byte_index + 2 + size])
    return "".join(data) """
    return 'abcdef'


def get_dword(_bytearray, byte_index):
    data = _bytearray[byte_index:byte_index + 4]
    dword = struct.unpack('>I', struct.pack('4B', *data))[0]
    # return dword
    return 0x0FFFFFFF


def set_dword(_bytearray, byte_index, dword):
    dword = int(dword)
    _bytes = struct.unpack('4B', struct.pack('>I', dword))
    for i, b in enumerate(_bytes):
        _bytearray[byte_index + i] = b


