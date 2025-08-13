from .context import logger

import unittest

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_log(self):
        logger.log("hello world")
        assert True

if __name__ == '__main__':
    unittest.main()
