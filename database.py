"""
DATABASE LOGGER
"""
import pyodbc
import tracer

#connStr = 'DRIVER={SQL Server};SERVER=T2RDTO38/WINCC;DATABASE=PLBDB1;UID=cimmgr;PWD=0proscon'
connStr = 'DSN=DataLogger_32;UID=cimmgr;PWD=0proscon'

def insertValues(table, tyonumero, map):
    insertTo = 'INSERT INTO cimmgr.' + table + ' '
    columns = '('
    values = ' VALUES ('

    for key in map:
        datatype = map[key]['datatype']
        if datatype == 'STRING':
            columns += key + ', '
            values += '\'' + str(map[key]['value']) + '\', '
        elif datatype == 'ARRAY OF REAL':
            array = map[key]['value']
            baseColumn = key[:-1]
            for i in range(0, len(array)):
                columns += baseColumn + str(i) + ', '
                values += str(array[i]) + ', '
        elif datatype == 'DATE_TIME':
            continue # SQL server generates timestamp automatically
        elif datatype == 'REAL' or datatype == 'INTEGER':
            columns += key + ', '
            values += str(map[key]['value']) + ', '

    columns = columns[:-2]
    values = values[:-2]

    columns += ')'
    values += ')'

    sqlQuery = insertTo + columns + values

    tracer.log(sqlQuery)

    __executeInsertQuery(table, sqlQuery)


def __executeInsertQuery(table, queryString):
    print("executeQuery")
    cnxn = pyodbc.connect(connStr)
    cursor = cnxn.cursor()
    cursor.execute(queryString)
    cursor.commit()
    
    """
    recordExists = 'SELECT (1) FROM cimmgr.{tb} WHERE AC1_KUVA_TYNO_VAL0={tn} AND AC1_KUVA_PINR_VAL0={pn}'.format(tb=table, tn=tyonumero, pn=pistonumero) 
    row = cursor.execute(recordExists).fetchone()
    if row is not None:
        print("Record exists")
    else:
        print("No record exists")
        cursor.execute(queryString)
        cursor.commit()
    """

def __testInsertValues():
    map = {
        'INTEGER_VAL0' : { 'datatype' : 'INTEGER', 'size' : '', 'value' : 1 },
        'REAL_VAL0' : { 'datatype' : 'REAL', 'size' : '', 'value' : 1.2  },
        'STRING_VAL0' : { 'datatype' : 'STRING', 'size' : '20', 'value' : 'abcd' },
        'ARRAY_VAL0' : { 'datatype' : 'ARRAY OF REAL', 'size' : '4', 'value' : [1.0, 2.0, 3.0, 4.0] },
        'DATETIME_VAL0' : { 'datatype' : 'DATE_TIME', 'size' : '8', 'value' : '' }
    }

    insertValues("TABLE", map)
 
def __test_executeInsertQuery():
    __executeInsertQuery('KUVA_KESTO', "INSERT INTO cimmgr.KUVA_KESTO (AC1_KUVA_TYNO_VAL0, AC1_KUVA_PINR_VAL0) VALUES (9001, 3)")

if __name__ == "__main__":
    # __testInsertValues()
    
    __test_executeInsertQuery()
    
    
    
