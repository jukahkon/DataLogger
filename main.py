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
plc_connection = False
previousStatusWord = 0
simulatedStatusWord = 0
tyonumero = 0
simulation = True

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
        simulatedStatusWord = simulatedStatusWord ^ 0x1000

def logTable(tableName):
    global tyonumero
    tyonumero = 0
    plcreader.clearCache()

    map = datamap.getTableMap(tableName)
    
    if map:
        for key in map:
            map[key]['value'] = plcreader.readTagValue(map[key])
        
        if 'AC1_KUVA_TYNO_VAL0' in map:
            tyonumero = map['AC1_KUVA_TYNO_VAL0']['value']

    if tyonumero:
        database.insertValues(tableName, tyonumero, map)
    else:
        print("TYO NUMERO PUUTTUU: " +tableName)

def checkPLCStatusAndLogData():
    global previousStatusWord
    global tyonumero

    if simulation:
        statusWord = simulatedStatusWord
    else:
        statusWord = plcreader.readValue('S7AreaMK', 0, 'INTEGER', 1008, 2)

    print("PLC STATUS: {0:b}".format(statusWord))

    # values that are logged once
    if statusWord != previousStatusWord:
        
        if statusWord & 0x1 and not (previousStatusWord & 0x1):
            print("KUVA NOPEAT TAULU VALMIS")
            logTable('KUVA_NOP01')
            logTable('KUVA_NOP02')
            logTable('KUVA_NOP03')
            logTable('KUVA_NOP04')
            logTable('KUVA_NOP05')
            logTable('KUVA_NOP06')
            logTable('KUVA_NOP07')
            logTable('KUVA_NOP08')
            logTable('KUVA_NOP09')
            logTable('KUVA_NOP10')
            
        if statusWord & 0x10 and not (previousStatusWord & 0x10):
            print("KUVA TIEDONKERUU AKTIVOITU")
            logTable('KUVA_PERUS')
            logTable('KUVA_RESEPTI1')
            logTable('KUVA_RESEPTI2')
            logTable('KUVA_TRD1')
            logTable('KUVA_TRD2')

        if statusWord & 0x100 and not (previousStatusWord & 0x100):
            print("PALA TIEDONKERUU AKTIVOITU")
            logTable('KYVA_PERUS')

        if statusWord & 0x400 and not (previousStatusWord & 0x400):
            print("KYVA NOPEAT TAULU VALMIS")
            logTable('KYVA_NOP01')
            logTable('KYVA_NOP02')
            logTable('KYVA_NOP03')
            logTable('KYVA_NOP04')
            logTable('KYVA_NOP05')
            logTable('KYVA_NOP06')
            logTable('KYVA_NOP07')
            logTable('KYVA_NOP08')
            logTable('KYVA_NOP09')
            logTable('KYVA_NOP10')

        if statusWord & 0x800 and not (previousStatusWord & 0x800):
            print("NAVA TIEDONKERUU AKTIVOITU")
            logTable('NAVA_PERUS')
            logTable('KUVA_TRD1')
        
        if statusWord & 0x1000 and not (previousStatusWord & 0x1000):
            print("LAKA TIEDONKERUU AKTIVOITU")
            logTable('LAKA_PERUS')
            logTable('LAKA_TRD1')
            logTable('LAKA_TRD2')

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
    global t_periodic, plc_connection

    if not plc_connection:
        try:
            plcreader.connect()
        except Exception as e:
            print("PLC connect failed: " +str(e))
            print("Retry ...")
        else:
            plc_connection = True

    if plc_connection:
        checkPLCStatusAndLogData()

    t_periodic = Timer(1 , tick_1s)
    t_periodic.setDaemon(True)
    t_periodic.start()


def main():
    print("DATA LOGGER STARTING, PRESS 'x' OR CTRL-c TO QUIT")
    global simulation
    sleep(1)
    datamap.readDataMapFile()
    
    tick_1s()

    c = ''

    while(c != b'x' and c != b'\x03'):
        c = readchar(blocking=True)

        if c == b's':
            simulation = not simulation
            # print("Simulation: " +str(simulation))

        if simulation:
            simulate(c)

    print("DATA LOGGER TERMINATING ...")
    if t_periodic:
        t_periodic.cancel()

    plcreader.disconnect()

main()
