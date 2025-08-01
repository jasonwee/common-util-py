# -*- coding: utf-8 -*-
"""mock database class"""

from unittest import TestCase
import os
import sys
import mysql.connector
from mysql.connector import errorcode
from .utils import get_config


MYSQL_USER = os.environ.get("MYSQL_USER", "testuser")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "mysql123")
MYSQL_DB = os.environ.get("MYSQL_DB", "testdb")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_PORT = os.environ.get("MYSQL_PORT", 3306)


class MockDB(TestCase):
    """
    The MockDB class is a mock database class used for setting up and tearing down
    a test MySQL database environment. It creates a database and a test table with
    initial data for testing purposes. The class also ensures that resources are
    cleaned up after tests are executed.

    Methods:
        setUpClass(cls): Sets up the test database and table, and inserts initial data.
        tearDownClass(cls): Cleans up by dropping the test database.
    """

    @classmethod
    def setUpClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, port=MYSQL_PORT
        )
        cursor = cnx.cursor(dictionary=True)

        # drop database if it already exists
        try:
            cursor.execute(f"DROP DATABASE IF EXISTS {MYSQL_DB}")
            cursor.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            print(f"{MYSQL_DB} does not exists. Dropping db failed {err}")

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(f"CREATE DATABASE {MYSQL_DB} DEFAULT CHARACTER SET 'utf8'")
        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
            sys.exit(1)
        cnx.database = MYSQL_DB

        query = """CREATE TABLE `test_table` (
                  `id` varchar(30) NOT NULL PRIMARY KEY ,
                  `text` text NOT NULL,
                  `int` int NOT NULL
                )"""
        try:
            cursor.execute(query)
            cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("test_table already exists.")
            else:
                print(err.msg)
        else:
            print("OK table created")

        insert_data_query = """INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('1', 'test_text', 1),
                            ('2', 'test_text_2',2)"""
        try:
            cursor.execute(insert_data_query)
            cnx.commit()
        except mysql.connector.Error as err:
            print("Data insertion to test_table failed \n" + err)
        else:
            print("mock data inserted")
            cursor.close()
            cnx.close()

        testconfig = {
            "host": MYSQL_HOST,
            "user": MYSQL_USER,
            "password": MYSQL_PASSWORD,
            "database": MYSQL_DB,
            "port": MYSQL_PORT,
        }
        cls.mock_db_config = get_config(testconfig)

    @classmethod
    def tearDownClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT,
        )
        cursor = cnx.cursor(dictionary=True)

        # drop test database
        try:
            cursor.execute(f"DROP DATABASE {MYSQL_DB}")
            cnx.commit()
        except mysql.connector.Error as err:
            print(f"Database {MYSQL_DB} does not exists. Dropping db failed " + err)
        finally:
            cnx.close()

        print("cleanup done")
