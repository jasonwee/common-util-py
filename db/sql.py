import pymysql as MySQLdb

from typing import Dict, List

# create table
def create_table(mysql_con: MySQLdb, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)

def drop_table(mysql_con: MySQLdb, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)

# load data
def insert(mysql_con: MySQLdb, table_name: str, data: Dict[str, str]) -> int:
    """
    values = ''.format
    fields = ''.format(data)
    for k, v in data.items():
        #sql = "INSERT INTO table (a, b) VALUES (%s, %s)"
        #val = ("123.456", "hihihi")
        pass
    """
    keys = data.keys()
    values = data.values()
    #sql_values_placeholder = '%s' * len(values)
    sql_values_placeholder = ', '.join(['%s']*len(values))
    sql_final = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(table_name, ', '.join(keys), sql_values_placeholder)
    cur = mysql_con.cursor()
    cur.execute(sql_final, list(values))
    return cur.rowcount

def insert_statement(mysql_con: MySQLdb, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)

def insert_rows(mysql_con: MySQLdb, table_name: str, rows: List[Dict]) -> None:
    for row in rows:
        insert(mysql_con, table_name, row)

def select_statement(mysql_con: MySQLdb, sql: str) -> List[Dict]:
    cur = mysql_con.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    return cur.fetchall()

def delete(mysql_con: MySQLdb, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)

def update(mysql_con: MySQLdb, table_name: str, data: Dict[str, str], condition: str) -> int:
    keys = data.keys()
    values = data.values()
    sql_values_placeholder = ', '.join([x+' = %s' for x in keys])
    #sql_final = 'UPDATE {0} SET '.format(table_name, ', '.join(keys), sql_values_placeholder)
    sql_final = 'UPDATE {0} SET {1} WHERE {2}'.format(table_name, sql_values_placeholder, condition)
    cur = mysql_con.cursor()
    cur.execute(sql_final, list(values))
    return cur.rowcount

def update_table(mysql_con: MySQLdb, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)

def generic(mysql_con: MySQLdb, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)
