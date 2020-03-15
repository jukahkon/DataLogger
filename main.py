"""
MAIN MODULE
"""
import datamap
import plcreader
import database
from pprint import pprint
from threading import Timer
from readchar import readchar
from time import sleep

t_periodic = None
previousStatusWord = 0
simulatedStatusWord = 0
simulation = True

def log_KUVA_PERUS():
    map = datamap.getTableMap('KUVA_PERUS')
    for key in map:
        map[key]['value'] = plcreader.readTagValue(map[key])
    
    database.insertValues('KUVA_PERUS', map)

def simulate(ch):
    global simulatedStatusWord

    if ch == b'1':
        simulatedStatusWord = simulatedStatusWord ^ 0x1
    elif ch == b'2':
        simulatedStatusWord = simulatedStatusWord ^ 0x10
    elif ch == b'3':
        simulatedStatusWord = simulatedStatusWord ^ 0x100    
    elif ch == b'4':
        simulatedStatusWord = simulatedStatusWord ^ 0x400    
    elif ch == b'5':
        simulatedStatusWord = simulatedStatusWord ^ 0x800    
    elif ch == b'6':
        simulatedStatusWord = simulatedStatusWord ^ 0b1000

def logValues():
    global previousStatusWord

    if simulation:
        statusWord = simulatedStatusWord
    else:
        statusWord = plcreader.readValue('S7AreaMK', 0, 'INTEGER', 1008, 2)

    # print("{0:b}".format(statusWord))

    # values that are logged once
    if statusWord != previousStatusWord:
        
        if statusWord & 0x1 and not (previousStatusWord & 0x1):
            print("KUVA NOPEAT TAULU VALMIS")

        if statusWord & 0x10 and not (previousStatusWord & 0x10):
            print("KUVA TIEDONKERUU AKTIVOITU")
            log_KUVA_PERUS()

        if statusWord & 0x100 and not (previousStatusWord & 0x100):
            print("PALA TIEDONKERUU AKTIVOITU")

        if statusWord & 0x400 and not (previousStatusWord & 0x400):
            print("KUVA NOPEAT TAULU VALMIS")

        if statusWord & 0x800 and not (previousStatusWord & 0x800):
            print("PALA TIEDONKERUU AKTIVOITU")
        
        if statusWord & 0x1000 and not (previousStatusWord & 0x1000):
            print("LAKA TIEDONKERUU AKTIVOITU")

        previousStatusWord = statusWord

    # values that are logged continuosly
    if statusWord & 0x10:
        # print("KUVA TRENDITIEDONKERUU")
        pass

    if statusWord & 0x100:
        # print("PALA TRENDITIEDONKERUU")
        pass

    if statusWord & 0x800:
        # print("PALA TRENDITIEDONKERUU")
        pass
        
    if statusWord & 0x1000:
        # print("LAKA TRENDITIEDONKERUU")
        pass


def tick_1s():
    global t_periodic

    logValues()

    t_periodic = Timer(1 , tick_1s)
    t_periodic.setDaemon(True)
    t_periodic.start()


def main():
    print("DATA LOGGER RUNNING, PRESS 'x' TO QUIT")
    global simulation
    sleep(1)
    datamap.readDataMapFile()
    plcreader.connect()
    tick_1s()

    c = ''

    while(c != b'x' and c != b'\x03'):
        c = readchar()

        if c == b's':
            simulation = not simulation
            print("Simulation: " +str(simulation))

        if simulation:
            simulate(c)

    print("DATA LOGGER TERMINATING ...")
    if t_periodic:
        t_periodic.cancel()

    plcreader.disconnect()


main()
