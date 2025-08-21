# -*- coding: UTF-8 -*-
"""db package conftest"""
import pytest


@pytest.fixture
def mock_mysql_connector(mocker):
    """Fixture to mock mysql.connector and its components."""
    # Create the mock connection and cursor
    mock_conn = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()

    # Set up the mock connection to return the mock cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.is_connected.return_value = True

    # Create a new mock for the connect function
    mock_connect = mocker.MagicMock(return_value=mock_conn)

    # Patch the mysql.connector.connect function
    mocker.patch("mysql.connector.connect", new=mock_connect)

    return mock_conn, mock_cursor, mock_connect
