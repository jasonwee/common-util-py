import pymysql as MySQLdb

from dataclasses import dataclass
from typing import Literal, Any



# create table
def create_table(mysql_con: MySQLdb.Connection, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)

def drop_table(mysql_con: MySQLdb.Connection, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)

# load data
def insert(mysql_con: MySQLdb.Connection, table_name: str, data: dict[str, str]) -> int:
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

def insert_statement(mysql_con: MySQLdb.Connection, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)

def insert_rows(mysql_con: MySQLdb.Connection, table_name: str, rows: list[dict[str, Any]]) -> None:
    for row in rows:
        insert(mysql_con, table_name, row)

@dataclass
class Condition:
    op: Literal['AND', 'OR']
    field: str
    cmp: Literal['=', '!=', '>', '<', '>=', '<=', 'LIKE', 'IN', 'NOT IN', 'IS NULL', 'IS NOT NULL']
    value: Any

def build_where_clause(conditions: list[Condition]) -> tuple[str, list[str]]:
    if not conditions:
        return "", []

    params: list[str] = []
    conditions_sql: list[str] = []

    for cond in conditions:
        if cond.cmp.upper() in ('IS NULL', 'IS NOT NULL'):
            conditions_sql.append(f"{cond.field} {cond.cmp}")
        else:
            conditions_sql.append(f"{cond.field} {cond.cmp} %s")
            params.append(cond.value)

    # The first condition's operator is ignored (usually starts with WHERE)
    where_clause = " WHERE " + " ".join(
        f"{cond.op} {conditions_sql[i]}"
        for i, cond in enumerate(conditions[1:], 1)
    )
    where_clause = where_clause.replace("WHERE AND", "WHERE").replace("WHERE OR", "WHERE")

    return where_clause, params

def select(
    mysql_con: MySQLdb.Connection,
    table_name: str,
    condition_groups: list[Condition] | None = None,
    field_names: list[str] | None = None
) -> list[dict[str, Any]]:
    """
    select * from table_name where foo = 'bar' or blah = "baz";
    """
    if field_names is None:
        field_names = ['*']
    if condition_groups is None:
        condition_groups = []

    fields = ', '.join(field_names)

    where_clause, params = build_where_clause(condition_groups)
    query = f"SELECT {fields} FROM {table_name}{where_clause}"

    with mysql_con.cursor(MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute(query, params)
        return list(cursor.fetchall())


def select_statement(mysql_con: MySQLdb.Connection, sql: str) -> list[dict[str, Any]]:
    cur = mysql_con.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    return list(cur.fetchall())

def delete(mysql_con: MySQLdb.Connection, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)

def update(mysql_con: MySQLdb.Connection, table_name: str, data: dict[str, str], condition: str) -> int:
    keys = data.keys()
    values = data.values()
    sql_values_placeholder = ', '.join([x+' = %s' for x in keys])
    #sql_final = 'UPDATE {0} SET '.format(table_name, ', '.join(keys), sql_values_placeholder)
    sql_final = 'UPDATE {0} SET {1} WHERE {2}'.format(table_name, sql_values_placeholder, condition)
    cur = mysql_con.cursor()
    cur.execute(sql_final, list(values))
    return cur.rowcount

def update_table(mysql_con: MySQLdb.Connection, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)

def generic(mysql_con: MySQLdb.Connection, sql: str) -> None:
    cur = mysql_con.cursor()
    cur.execute(sql)
