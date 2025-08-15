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
from collections.abc import Iterator
import mysql.connector
from mysql.connector import Error, MySQLConnection
from mysql.connector.cursor import MySQLCursor
from .database import TransactionError, sanitize_identifier


class Mysql:
    """A simplified MySQL database wrapper for CRUD operations.

    Example:
    with Mysql(host='localhost', user='user', password='pass', database='mydb') as db:
        db.create("CREATE TABLE IF NOT EXISTS test"
                  "(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
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
        """create database or table"""
        cursor = self.conn.cursor()
        if vals:
            cursor.execute(statement, vals)
            self.conn.commit()
        else:
            cursor.execute(statement)
        return cursor.rowcount

    def batch_insert(
        self,
        table: str,
        columns: list[str],
        data: list[tuple],
        batch_size: int = 1000,
        on_duplicate_key_update: bool = False,
        update_columns: list[str] | None = None,
    ) -> int:
        """Perform a batch insert operation."""
        if not data:
            return 0

        if not columns:
            raise ValueError("columns cannot be empty")

        # Sanitize all identifiers
        safe_table = sanitize_identifier(table)
        safe_columns = [sanitize_identifier(col) for col in columns]

        # Verify no columns were completely removed by sanitization
        if not safe_table or not all(safe_columns):
            raise ValueError("Invalid table or column names provided")

        # Build the column list part of the query with backticks
        columns_str = ", ".join(f"`{col}`" for col in safe_columns)
        placeholders = ", ".join(["%s"] * len(safe_columns))

        # Build the basic INSERT query with backticks
        query = f"INSERT INTO `{safe_table}` ({columns_str}) VALUES ({placeholders})"

        # Add ON DUPLICATE KEY UPDATE if needed
        if on_duplicate_key_update:
            if update_columns is None:
                update_columns = safe_columns
            else:
                # Sanitize update_columns if provided
                update_columns = [sanitize_identifier(col) for col in update_columns]
                if not all(update_columns):
                    raise ValueError("Invalid update_columns provided")

            update_clause = ", ".join(
                f"`{col}` = VALUES(`{col}`)" for col in update_columns
            )
            query += f" ON DUPLICATE KEY UPDATE {update_clause}"

        # Process in batches to avoid very large queries
        total_affected = 0
        cursor = self.conn.cursor()

        try:
            for i in range(0, len(data), batch_size):
                batch = data[i : i + batch_size]
                cursor.executemany(query, batch)
                total_affected += cursor.rowcount

            self.conn.commit()
            return total_affected

        except Error as e:
            self.conn.rollback()
            raise Exception(f"Batch insert failed: {e}") from e
        finally:
            cursor.close()

    def read(self, statement: str, vals: tuple = ()) -> list[dict]:
        """read rows from table"""
        cursor = self.conn.cursor()
        try:
            if vals:
                cursor.execute(statement, vals)
            else:
                cursor.execute(statement)
            results = cursor.fetchall()
            return results
        except Error as e:
            # maybe here can raise a custom error, example DatabaseError
            raise Exception(f"Failed to read from MySQL: {e}") from e

    def update(self, statement: str, vals: tuple = ()) -> int:
        """update rows in table"""
        cursor = self.conn.cursor()
        if vals:
            cursor.execute(statement, vals)
        else:
            cursor.execute(statement)
        self.conn.commit()
        return cursor.rowcount

    def batch_update(
        self,
        table: str,
        update_columns: list[str],
        where_columns: list[str],
        data: list[tuple],
        batch_size: int = 1000,
    ) -> int:
        """Perform a batch update operation."""
        if not data:
            return 0

        # Validate input
        if not update_columns or not where_columns:
            raise ValueError("update_columns and where_columns cannot be empty")

        # Sanitize all identifiers
        safe_table = sanitize_identifier(table)
        safe_update_columns = [sanitize_identifier(col) for col in update_columns]
        safe_where_columns = [sanitize_identifier(col) for col in where_columns]

        # Verify no columns were completely removed by sanitization
        if (
            not safe_table
            or not all(safe_update_columns)
            or not all(safe_where_columns)
        ):
            raise ValueError("Invalid table or column names provided")

        # Build the SET part of the query
        set_clause = ", ".join(f"{col} = %s" for col in safe_update_columns)

        # Build the WHERE part of the query
        where_clause = " AND ".join(f"{col} = %s" for col in safe_where_columns)

        # Build the full query
        query = f"UPDATE {safe_table} SET {set_clause} WHERE {where_clause}"

        # Process in batches to avoid very large queries
        total_affected = 0
        cursor = self.conn.cursor()
        try:
            for i in range(0, len(data), batch_size):
                batch = data[i : i + batch_size]
                # Convert each row's data into the correct parameter order
                # (update_values first, then where_values)
                params = list(batch)
                cursor.executemany(query, params)
                total_affected += cursor.rowcount

            self.conn.commit()
            return total_affected
        except Error as e:
            self.conn.rollback()
            raise Exception(f"Batch update failed: {e}") from e
        finally:
            cursor.close()

    def delete(self, statement: str, vals: tuple = ()) -> int:
        """Delete rows from table"""
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

    @contextmanager
    def transaction(
        self, rollback_on: type[Exception] | tuple[type[Exception], ...] | None = None
    ) -> Iterator[None]:
        """context manager for handling database transactions."""
        if rollback_on is None:
            # Default: rollback on any exception
            rollback_on = (Exception,)

        try:
            # Start transaction
            self.conn.start_transaction()

            # Execute the code inside the with block
            yield

            # If we get here, commit the transaction
            self.conn.commit()

        except rollback_on:
            # Rollback on specified exceptions
            try:
                self.conn.rollback()
            except Error as rollback_err:
                # If rollback fails, raise a TransactionError
                raise TransactionError(
                    "Failed to rollback transaction"
                ) from rollback_err
            # Re-raise the original exception
            raise

        except Exception:
            # For any other exception, rollback if not in autocommit mode
            if not self.conn.autocommit:
                try:
                    self.conn.rollback()
                except Error as rollback_err:
                    raise TransactionError(
                        "Failed to rollback transaction"
                    ) from rollback_err
            # Re-raise the original exception
            raise
