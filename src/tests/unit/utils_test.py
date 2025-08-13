# -*- coding: utf-8 -*-
"""utils test module"""
import pytest
from .mock_db import MockDB
from . import utils


@pytest.fixture(scope="class", autouse=True)
def setup_mock_db():
    """setup mock DB"""
    # Setup the mock DB before tests
    MockDB.setUpClass()
    yield
    # Teardown the mock DB after tests
    MockDB.tearDownClass()


def test_db_write():
    """test db_write function"""
    assert (
        utils.db_write(
            """INSERT INTO `test_table` (`id`, `text`, `int`) VALUES ('3', 'test_text_3', 3)"""
        )
        is True
    )
    assert (
        utils.db_write(
            """INSERT INTO `test_table` (`id`, `text`, `int`) VALUES ('1', 'test_text_3', 3)"""
        )
        is False
    )
    assert utils.db_write("""DELETE FROM `test_table` WHERE id='1' """) is True
    assert utils.db_write("""DELETE FROM `test_table` WHERE id='4' """) is True
