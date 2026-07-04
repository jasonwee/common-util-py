from common_util_py.logger import log

import unittest

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_log(self):
        log("hello world")
        assert True

if __name__ == '__main__':
    unittest.main()
