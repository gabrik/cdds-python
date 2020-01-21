import unittest

__author__ = 'ADlink Technology'

from pydds import *
import time

class BasicTestCase(unittest.TestCase):
    def test_participant(self):
        dp = Participant(0)
        
        self.assertTrue( dp is not None ) 
        self.assertIsInstance(dp, Participant)

if __name__ == "__main__":
    unittest.main() # run all tests
