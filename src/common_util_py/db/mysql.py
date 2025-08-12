# -*- coding: UTF-8 -*-
#
#   Copyright WeeTech Developer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
mysql database class
"""

from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error, MySQLConnection
from mysql.connector.cursor import MySQLCursor


class Mysql:
    """A simplified MySQL database wrapper for CRUD operations.

    Example:
        with Mysql(host='localhost', user='user', password='pass', database='mydb') as db:
            db.create("CREATE TABLE IF NOT EXISTS test (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
    """

    def __init__(self, host: str, username: str, password: str, **kwargs):
        """Initialize MySQL database connection"""
        self.connection_params = {
            "host": host,
            "user": username,
            "password": password,
            **kwargs,
        }
        self.conn: MySQLConnection | None = None
        self.connect()

    def connect(self) -> None:
        """Establish database connection."""
        try:
            self.conn = mysql.connector.connect(**self.connection_params)
        except Error as e:
            raise ConnectionError(f"Failed to connect to MySQL: {e}") from e

    def close(self) -> None:
        """Close the database connection."""
        if self.conn and self.conn.is_connected():
            self.conn.close()

    def __enter__(self) -> "Mysql":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def create(self, statement: str, vals: tuple = ()) -> int:
        """
        create database or table
        # create database mydb
        # show databases
        # CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))
        #"INSERT INTO customers (name, address) VALUES (%s, %s)" | ("John", "Highway 21")
        # "DROP TABLE customers"
        # "DROP TABLE IF EXISTS customers"
        """
        cursor = self.conn.cursor()
        if vals:
            cursor.execute(statement, vals)
            self.conn.commit()
        else:
            cursor.execute(statement)
        return cursor.rowcount

    def read(self, statement: str, vals: tuple = ()) -> list[dict]:
        """
        read rows from table
        SELECT * FROM customers
        SELECT name, address FROM customers
        SELECT * FROM customers WHERE address ='Park Lane 38'
        SELECT * FROM customers WHERE address = %s | ("Yellow Garden 2", )
        SELECT * FROM customers ORDER BY name
        SELECT * FROM customers ORDER BY name DESC
        SELECT * FROM customers LIMIT 5
        SELECT * FROM customers LIMIT 5 OFFSET 2
        "SELECT users.name AS user, products.name AS favorite FROM users INNER JOIN products ON users.fav = products.id
        """
        cursor = self.conn.cursor()
        if vals:
            cursor.execute(statement, vals)
        else:
            cursor.execute(statement)
        results = cursor.fetchall()
        return results

    def update(self, statement: str, vals: tuple = ()) -> int:
        """
        update rows in table
        # "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
        # "UPDATE customers SET address = %s WHERE address = %s" | ("Valley 345", "Canyon 123")
        """
        cursor = self.conn.cursor()
        if vals:
            cursor.execute(statement, vals)
        else:
            cursor.execute(statement)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, statement: str, vals: tuple = ()) -> int:
        """
        Delete rows from table
        # DELETE FROM customers WHERE address = 'Mountain 21'
        # DELETE FROM customers WHERE address = %s | ("Yellow Garden 2", )
        """
        cursor = self.conn.cursor()
        if vals:
            cursor.execute(statement, vals)
        else:
            cursor.execute(statement)
        self.conn.commit()
        return cursor.rowcount

    @contextmanager
    def cursor(self, dictionary: bool = False) -> MySQLCursor:
        """Get a database cursor with context manager."""
        if not self.conn or not self.conn.is_connected():
            self.connect()

        cursor = self.conn.cursor(dictionary=dictionary)
        try:
            yield cursor
        finally:
            cursor.close()
