import unittest

__author__ = 'ADlink Technology'

from cdds import *

import time

class EntityTest (unittest.TestCase):
    def setUp(self):
        self.rt = Runtime.get_runtime()
        # entity = Entity()

        
    def test_create_entity(self):
        e = Participant(0)
        self.assertIsNotNone(e, "Created entity is not initialized correctly")
        self.assertIsInstance(e, Entity, "Created object is not of the correct type")
    
    def test_set_parent_get_parent(self):
        dp = Participant(0)
        self.assertEqual(dp, dp.parent)
        
        topic_name = 'topic_name'
         
        topic = dp.create_topic(topic_name)
        parent_entity = topic.parent
        self.assertIsNotNone(parent_entity, " Get parent on a topic entity returned null")
        self.assertEqual(parent_entity, dp)
        
        pub = dp.create_publisher()
        parent_entity = pub.participant
        self.assertIsNotNone(parent_entity, " Get parent on a publisher entity returned null")
        self.assertEqual(parent_entity, dp, "Get parent on a publisher entity a wrong entity")
        
        sub = dp.create_subscriber()
        parent_entity = sub.parent
        self.assertIsNotNone(parent_entity, " Get parent on a subscriber entity returned null")
        self.assertEqual(dp, parent_entity, "Get parent on a subscriber entity returned a wrong entity")
        
        dw = pub.create_writer(topic)
        parent_entity = dw.parent
        self.assertIsNotNone(parent_entity, " Get parent on a datawriter entity returned null")
        self.assertEqual(parent_entity, pub, "Get parent on a datawriter entity a wrong entity")
        
        dr = sub.create_reader(topic)
        parent_entity = dr.parent
        self.assertIsNotNone(parent_entity, " Get parent on a datareader entity returned null")
        self.assertEqual(parent_entity, sub, "Get parent on a datareader entity a wrong entity")
        
    def test_set_participant_get_participant(self):
        dp = Participant(0)
        
        self.assertEqual(dp, dp.participant)
        
        topic_name = 'topic_name'
         
        topic = dp.create_topic(topic_name)

        entity = topic.participant
         
        self.assertIsNotNone(entity, " Get participant on a topic entity returned null")
        self.assertEqual(entity, dp, "Get participant on a topic entity returned a wrong result")
        
        pub = dp.create_publisher()
        entity = pub.participant
        self.assertIsNotNone(entity, " Get participant on a publisher entity returned null")
        self.assertEqual(entity, dp, "Get participant on a publisher entity a wrong entity")
        
        sub = dp.create_subscriber()
        entity = sub.participant
        self.assertIsNotNone(entity, " Get participant on a subscriber entity returned null")
        self.assertEqual(dp, entity, "Get participant on a subscriber entity returned a wrong entity")
        
        dw = pub.create_writer(topic)
        entity = dw.participant
        self.assertIsNotNone(entity, " Get participant on a datawriter entity returned null")
        self.assertEqual(entity, dp, "Get participant on a datawriter entity a wrong entity")
        
        dr = sub.create_reader(topic)
        entity = dr.participant
        self.assertIsNotNone(entity, " Get participant on a datareader entity returned null")
        self.assertEqual(entity, dp, "Get participant on a datareader entity a wrong entity")
        
        
    
if __name__ == "__main__":
    unittest.main() # run all tests