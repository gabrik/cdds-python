import unittest



__author__ = 'ADlink Technology'

from cdds import *
import cdds.py_dds_utils as utils


import time

class ParticipantBasicTest (unittest.TestCase):
    def setUp(self):
        self.rt = Runtime.get_runtime()
        
        self.dp = Participant(0)
        
        self.topic_name = "topic_name"
        self.type_support = self.rt.get_key_value_type_support() 
        self.topic = self.dp.create_topic(self.topic_name, self.type_support)
        
    def test_create_participant(self):
        """
        Test that the participant can be created successfully
        """
        participant = Participant(0)
        self.assertTrue( participant is not None ) 
        self.assertIsInstance(participant, Participant)
        
    def test_create_topic(self):
        """
        test create topic
        """
        other_topic_name = "other_topic_name"
        other_topic = self.dp.create_topic(other_topic_name, self.type_support)
                
        self.assertTrue(other_topic is not None, "Could not create topic")
        
    def test_find_topic(self):
        """
        test find topic
        """
        foundTopic = self.dp.find_topic("topic_name")
        
        if(foundTopic is not None):
            topic_to_test = utils._FoundTopic_Init(self.dp, foundTopic)
        else:
            topic_to_test = None
            
        found_topic_name = topic_to_test.get_name()
        self.assertTrue(topic_to_test is not None, "Found topic should not be none")
        # self.assertEqual(self.topic.topic, foundTopic, "Find topic failed")
        
        self.assertEqual(self.topic.name, found_topic_name, "Find using name failed")
        
    def test_create_publisher(self):
        """
        Test create publisher
        """
        participant = Participant(0)
        pub = participant.create_publisher()
        self.assertTrue( pub is not None )
        self.assertTrue(pub.handle > 0, "Failed to create a publisher") 
        
    def test_create_subscriber(self):
        """
        Test create subscriber
        """
        participant = Participant(0)
        sub = participant.create_subscriber()
        self.assertTrue( sub is not None ) 
        self.assertTrue( sub.handle > 0, "Failed to create a subscriber")
    
if __name__ == "__main__":
    unittest.main() # run all tests
