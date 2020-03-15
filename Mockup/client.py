"""
Snap7 client used for connection to a siemens7 server.
"""
import re
from ctypes import c_int, c_char_p, byref, sizeof, c_uint16, c_int32, c_byte
from ctypes import c_void_p

import logging

import snap7
from snap7 import six
from snap7.snap7types import S7Object, buffer_type, buffer_size, BlocksList
from snap7.snap7types import TS7BlockInfo, param_types, cpu_statuses

from snap7.common import check_error, load_library, ipv4
from snap7.snap7exceptions import Snap7Exception

logger = logging.getLogger(__name__)


def error_wrap(func):
    """Parses a s7 error code returned the decorated function."""
    def f(*args, **kw):
        code = func(*args, **kw)
        check_error(code, context="client")
    return f

class Client(object):
    """
    A snap7 client
    """
    pointer = None
    library = None

    def __init__(self):
        self.create()

    def __del__(self):
        self.destroy()
        
    def create(self):
        print("Snap7 client create")
    
    def destroy(self):
        print("Snap7 client destroy")

    def disconnect(self):
        print("Snap7 client disconnect")

    def connect(self, address, rack, slot, tcpport=102):
        print("Snap7 client connect: " +address)

    def read_area(self, area, dbnumber, start, size):
        print("Client::read_area: " + str(area) + " " + str(dbnumber) + " " + str(size) + " " + str(size))
        return b'0000'

