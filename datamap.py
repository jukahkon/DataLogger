"""
DATA MAP
"""
from pprint import pprint
import codecs

fileName = './Data/datamap.csv'
csvDelimiter = ';'
dataMap = {}

def getTableMap(table):
    if table in dataMap:
        return dataMap[table]
    else:
        return {}

def readDataMapFile():
    with codecs.open(fileName, encoding='utf-8') as f_in:
        # print("Luetaan tiedosto: " +fileName)
        lines = f_in.readlines()

        lineNbr = 0

        for line in lines:
            (table, column, title, datatype, area, db, offset, size) = line.split(csvDelimiter)

            lineNbr += 1

            if lineNbr < 2 or len(line) < 1:
                continue

            # print(line)
            table = table.strip()
            column = column.strip()
            size = size.strip()

            if size:
                dSize = int(size)
            else:
                dSize = 0

            if db:
                dDb = int(db)
            else:
                dDb = 0

            if offset:
                dOffset = int(offset)
            else:
                dOffset = 0

            if not table in dataMap:
                dataMap[table] = {}
            elif not column in dataMap[table]:
                dataMap[table][column] = {
                    'title' : title,
                    'datatype' : datatype,
                    'area' : area,
                    'db' : dDb,
                    'offset' : int(dOffset),
                    'size' : dSize,
                }
            else:
                print("Duplicate entry in datamap csv, line: " + lineNbr + " +column")
            

if __name__ == "__main__":
    readDataMapFile()
    pprint(dataMap['KUVA_PERUS']['AC1_KUVA_AVHA_VAL0'])
    pprint(dataMap['KUVA_TRD1']['AC1_M069_PV_VAL0'])
    pprint(dataMap['KUVA_NOP01']['AC1_KUVA_NOP01_VAL0'])
    pprint(dataMap['KUVA_RESEPTI1']['AC1_KUVA_01ULRU_VAL0'])
    pprint(dataMap['LAKA_TRD2']['AC1_C092_PV_VAL0'])

