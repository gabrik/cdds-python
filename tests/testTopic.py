import unittest
from cdds import *
from cdds.py_dds_utils import *

__author__ = 'ADlink Technology'

import time

class TopicTest (unittest.TestCase):
    def setUp(self):
        self.rt = Runtime.get_runtime()
        self.dp = Participant(0)
        self.name = "topic_name"
        self.type_support = self.rt.get_hello_world_simple_value_type_support()
        self.topic = Topic (self.dp, self.name, self.type_support , None, None, None)
        
    def tearDown(self):
        self.dp.rt.close()
        pass
        
    def test_create_topic_based_on_topic_desc (self):
        """
        test create topic desc
        """
        self.assertTrue(self.topic is not None, "Create Topic failed")
        self.assertIsInstance(self.topic, Topic, "created topic is not of the valid class (Topic)")
        
#     def test_try_gen_class(self):
#         get_dds_classes_from_idl('/home/firas/cyclone/cdds_python/tests/example.idl', 'HelloWorldData.Msg')
#         
#         #self.assertTrue(gen_info is not None)
        
    def test_get_name(self):
        result_topic_name = ""
        get_name = self.topic.name
        self.assertEqual(get_name, self.topic.name, "Wrong topic name returned from property name")
    
    def test_get_type_name(self):
        expected_topic_name = "HelloWorldData::Msg"
        get_name = self.topic.type_name()
        self.assertEqual(get_name, expected_topic_name, "Wrong topic type name returned ")
        
if __name__ == "__main__":
    unittest.main() # run all tests