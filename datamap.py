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

            if not table in dataMap:
                dataMap[table] = {}
            elif not column in dataMap[table]:
                dataMap[table][column] = {
                    'title' : title,
                    'datatype' : datatype,
                    'area' : area,
                    'db' : db,
                    'offset' : offset,
                    'size' : size.strip(),
                }
            else:
                print("Duplicate entry in datamap csv, line: " + lineNbr + " +column")
            

if __name__ == "__main__":
    readDataMapFile()
    pprint(dataMap)


