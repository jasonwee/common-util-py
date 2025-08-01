# -*- coding: utf-8 -*-
"""utils module"""

import os
import pymysql as MySQLdb
import mysql.connector
from mysql.connector import errorcode

config = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "user": os.environ.get("MYSQL_USER", "testuser"),
    "password": os.environ.get("MYSQL_PASSWORD", "mysql123"),
    "database": os.environ.get("MYSQL_DB", "testdb"),
    "port": os.environ.get("MYSQL_PORT", 3306),
}


def get_config(p_config=None):
    """get config"""
    default_config = {
        "host": "MYSQL_HOST",
        "user": "MYSQL_USER",
        "password": "MYSQL_PASSWORD",
        "database": "MYSQL_DB",
        "port": "MYSQL_PORT",
    }
    return p_config or default_config


def db_read(query, params=None) -> list | None:
    """read from database"""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        entries = cursor.fetchall()
        cursor.close()
        cnx.close()

        content = []

        for entry in entries:
            content.append(entry)

        return content

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User authorization error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist")
        else:
            print(err)
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("Connection closed")
    return None


def db_write(query, params=None) -> bool:
    """write to database"""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            cnx.commit()
            cursor.close()
            cnx.close()
            return True

        except MySQLdb.Error:
            cursor.close()
            cnx.close()
            return False

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User authorization error")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist")
        else:
            print(err)
        return False
