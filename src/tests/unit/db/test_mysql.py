# -*- coding: UTF-8 -*-
"""test mysql"""

from unittest.mock import patch
import pytest
import mysql.connector
from common_util_py.db import mysql as cmysql

# Sample test data
SAMPLE_CONFIG = {
    "host": "test_host",
    "username": "test_user",
    "password": "test_pass",
    "database": "test_db",
}


def test_initialization(mock_mysql_connector):
    """Test that Mysql class initializes with correct parameters."""
    _, _, mock_connect = mock_mysql_connector

    # Test with minimal parameters
    db = cmysql(host="test", username="user", password="pass")
    # Connection is lazy, so no connect call yet
    mock_connect.assert_not_called()

    # Now trigger a connection
    with db.cursor():
        pass

    # Now it should have connected with the right parameters
    mock_connect.assert_called_once_with(
        host="test",
        user="user",
        password="pass",
    )


def test_connection_handling(mock_mysql_connector):
    """Test connection management."""
    mock_conn, _, mock_connect = mock_mysql_connector

    # Create instance - no connection attempt yet
    db = cmysql(**SAMPLE_CONFIG)
    mock_connect.assert_not_called()

    # First database operation - should establish connection
    with db.cursor() as cursor:
        # The actual connection is made when cursor is created
        mock_connect.assert_called_once()

        # Reset the mock to track subsequent calls
        mock_connect.reset_mock()

        # Execute a query
        cursor.execute("SELECT 1")

        # The connection should be reused, not created again
        mock_connect.assert_not_called()

    # Reset mocks for reconnection test
    mock_connect.reset_mock()
    mock_conn.is_connected.return_value = False

    # Test reconnection when connection is lost
    with db.cursor() as cursor:
        # Should detect lost connection and reconnect
        cursor.execute("SELECT 1")

        # Should have called connect again for reconnection
        # mock_connect.assert_called_once()
        # Should have called connect again for reconnection
        assert mock_connect.call_count == 1


def test_cursor_context_manager(mock_mysql_connector):
    """Test cursor context manager behavior."""
    mock_conn, mock_cursor, _ = mock_mysql_connector

    # Test regular cursor
    with cmysql(**SAMPLE_CONFIG) as db:
        with db.cursor() as cursor:
            cursor.execute("SELECT 1")
            mock_cursor.execute.assert_called_once_with("SELECT 1")
        assert mock_cursor.close.called

    # Test dictionary cursor
    with cmysql(**SAMPLE_CONFIG) as db:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT 1")
            mock_conn.cursor.assert_called_with(dictionary=True)


def test_create_operation(mock_mysql_connector):
    """
    Test create/insert operations.

    create database mydb
    show databases
    CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))
    INSERT INTO customers (name, address) VALUES (%s, %s)" | ("John", "Highway 21")
    DROP TABLE customers"
    DROP TABLE IF EXISTS customers"
    """
    mock_conn, mock_cursor, _ = mock_mysql_connector
    mock_cursor.rowcount = 1

    db = cmysql(**SAMPLE_CONFIG)

    # Test simple create
    result = db.create("CREATE TABLE test (id INT)")
    assert result == 1
    mock_cursor.execute.assert_called_once_with("CREATE TABLE test (id INT)")

    # Test with parameters
    mock_cursor.reset_mock()
    db.create("INSERT INTO test VALUES (%s, %s)", (1, "test"))
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO test VALUES (%s, %s)", (1, "test")
    )
    assert mock_conn.commit.called


def test_read_operation(mock_mysql_connector):
    """
    Test read/select operations.

    SELECT * FROM customers
    SELECT name, address FROM customers
    SELECT * FROM customers WHERE address ='Park Lane 38'
    SELECT * FROM customers WHERE address = %s | ("Yellow Garden 2", )
    SELECT * FROM customers ORDER BY name
    SELECT * FROM customers ORDER BY name DESC
    SELECT * FROM customers LIMIT 5
    SELECT * FROM customers LIMIT 5 OFFSET 2
    SELECT users.name AS user, products.name AS favorite FROM users INNER JOIN
    products ON users.fav = products.id
    """
    _, mock_cursor, _ = mock_mysql_connector
    expected_result = [{"id": 1, "name": "test"}]
    mock_cursor.fetchall.return_value = expected_result

    db = cmysql(**SAMPLE_CONFIG)

    # Test simple read
    result = db.read("SELECT * FROM test")
    assert result == expected_result
    mock_cursor.execute.assert_called_once_with("SELECT * FROM test")
    mock_cursor.fetchall.assert_called_once()

    # Test with parameters
    mock_cursor.reset_mock()
    db.read("SELECT * FROM test WHERE id = %s", (1,))
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM test WHERE id = %s", (1,)
    )


def test_update_operation(mock_mysql_connector):
    """
    Test update operations.

    UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
    UPDATE customers SET address = %s WHERE address = %s" | ("Valley 345", "Canyon 123")
    """
    mock_conn, mock_cursor, _ = mock_mysql_connector
    mock_cursor.rowcount = 1

    db = cmysql(**SAMPLE_CONFIG)

    # Test update
    result = db.update("UPDATE test SET name = %s WHERE id = %s", ("new_name", 1))
    assert result == 1
    mock_cursor.execute.assert_called_once_with(
        "UPDATE test SET name = %s WHERE id = %s", ("new_name", 1)
    )
    assert mock_conn.commit.called


def test_delete_operation(mock_mysql_connector):
    """
    Test delete operations.

    DELETE FROM customers WHERE address = 'Mountain 21'
    DELETE FROM customers WHERE address = %s | ("Yellow Garden 2", )
    """
    mock_conn, mock_cursor, _ = mock_mysql_connector
    mock_cursor.rowcount = 1

    db = cmysql(**SAMPLE_CONFIG)

    # Test delete
    result = db.delete("DELETE FROM test WHERE id = %s", (1,))
    assert result == 1
    mock_cursor.execute.assert_called_once_with("DELETE FROM test WHERE id = %s", (1,))
    assert mock_conn.commit.called


def test_transaction_handling(mock_mysql_connector):
    """Test transaction management."""
    mock_conn, _, _ = mock_mysql_connector

    with cmysql(**SAMPLE_CONFIG) as db:
        with db.transaction():
            db.create("INSERT INTO test VALUES (1, 'test')")
            db.update("UPDATE test SET name = 'updated' WHERE id = 1")

        # Should commit on successful transaction
        assert mock_conn.commit.called
        assert not mock_conn.rollback.called

        # Test rollback on exception
        mock_conn.commit.reset_mock()
        try:
            with db.transaction():
                db.create("INSERT INTO test VALUES (2, 'test2')")
                raise Exception("Test error")
        except Exception:
            pass

        assert mock_conn.rollback.called
        assert not mock_conn.commit.called


def test_batch_operations(mock_mysql_connector):
    """Test batch insert/update operations."""
    _, mock_cursor, _ = mock_mysql_connector
    mock_cursor.rowcount = 2

    db = cmysql(**SAMPLE_CONFIG)

    # Test batch insert
    data = [(1, "test1"), (2, "test2")]
    result = db.batch_insert("test", ["id", "name"], data)
    # 2 rows
    assert result == 2
    assert mock_cursor.executemany.called

    # Test batch update
    mock_cursor.reset_mock()
    data = [("new1", 1), ("new2", 2)]
    result = db.batch_update("test", ["name"], ["id"], data)
    # 2 rows
    assert result == 2


def test_connection_retry(mock_mysql_connector):
    """Test connection retry logic."""
    mock_conn, _, mock_connect = mock_mysql_connector

    # First call fails, second succeeds
    mock_conn.is_connected.side_effect = [False, True]

    # Don't actually sleep during tests
    with patch("time.sleep"):
        db = cmysql(**SAMPLE_CONFIG)
        db.connect()

        # This will trigger the retry
        with db.cursor():
            pass

    # Verify is_connected was called
    assert mock_conn.is_connected.called

    # Should have connected twice (initial + retry)
    assert mock_connect.call_count == 2


def test_error_handling(mock_mysql_connector):
    """Test error handling and logging."""
    _, mock_cursor, _ = mock_mysql_connector
    mock_cursor.execute.side_effect = mysql.connector.Error("Test error")

    db = cmysql(**SAMPLE_CONFIG)

    with pytest.raises(Exception, match="Failed to read from MySQL: Test error"):
        db.read("SELECT * FROM non_existent")
