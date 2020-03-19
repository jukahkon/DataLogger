"""
DATABASE LOGGER
"""
import pyodbc

connStr = 'DRIVER={SQL Server};SERVER=DESKTOP-56JU3BD/SQLEXPRESS;DATABASE=PLBDB1;UID=cimmgr;PWD=0proscon'

def insertValues(table, map):
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

    command = insertTo + columns + values

    print(command)

    #cnxn = pyodbc.connect(connStr)
    #cnxn.setencoding(encoding='utf-8')
    #cursor = cnxn.cursor()
    #cursor.execute("insert into cimmgr.KUVA_KESTO (AC1_KUVA_TYNO_VAL0, AC1_KUVA_PINR_VAL0) VALUES (13, 3)")
    #cnxn.commit()


if __name__ == "__main__":
    
    map = {
        'INTEGER_VAL0' : { 'datatype' : 'INTEGER', 'size' : '', 'value' : 1 },
        'REAL_VAL0' : { 'datatype' : 'REAL', 'size' : '', 'value' : 1.2  },
        'STRING_VAL0' : { 'datatype' : 'STRING', 'size' : '20', 'value' : 'abcd' },
        'ARRAY_VAL0' : { 'datatype' : 'ARRAY OF REAL', 'size' : '4', 'value' : [1.0, 2.0, 3.0, 4.0] },
        'DATETIME_VAL0' : { 'datatype' : 'DATE_TIME', 'size' : '8', 'value' : '' }
    }

    insertValues("TABLE", map)
 
