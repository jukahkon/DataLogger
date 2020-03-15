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
        columns += key + ', '
        if map[key]['datatype'] == 'STRING':
            values += '\'' + str(map[key]['value']) + '\', '
        else:
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
        'COLUMN_1' : { 'datatype' : 'INTEGER', 'size' : '', 'value' : 1 },
        'COLUMN_2' : { 'datatype' : 'REAL', 'size' : '', 'value' : 1.2  },
        'COLUMN_3' : { 'datatype' : 'STRING', 'size' : '20', 'value' : 'abcd' }
    }

    insertValues("TABLE", map)
 
