import unittest
from psutil.tests.runner import ctypes


__author__ = 'ADlink Technology'

from pydds import *
import pydds.py_dds_utils as utils

class SubscriberTest (unittest.TestCase):
    def setUp(self):
        self.rt = Runtime.get_runtime()
        self.participant = Participant(0)
        self.subscriber = Subscriber(self.participant)

    def test_initialize_subscriber(self):
        dp = Participant(0)
        sub = Subscriber(dp)
        self.assertIsNotNone(sub, "Subscriber is not created correctly")
        self.assertIsInstance(sub, Subscriber, "Create subscriber didn't produce an entity of the food type")
        
    def test_create_reader(self):
        topic_name = "topic_name"
        type_support = self.rt.get_key_value_type_support() 
        topic = Topic (self.participant, topic_name, type_support)
        datareader_ps = [Reliable(), KeepLastHistory(10)] 
        datareader = self.subscriber.dds_create_reader( topic, datareader_ps)
        
        self.assertIsNotNone( datareader, "Create_reader failed")
        self.assertIsInstance( datareader, Reader, "Create_dataReader created an entity of a wrong type")
        
    

if __name__ == "__main__":
    unittest.main() # run all tests