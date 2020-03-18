import unittest


# from cdds.py_dds_utils import *

__author__ = 'ADlink Technology'

from cdds import *

import time

# def _get_dds_descriptor_from_idl(idl_path, type_name):
#     """ Return DDS Type descriptor from IDL file
# 
#     :type idl_path: string
#     :param idl_path: path to the IDL file
# 
#     :type type_name: string
#     :param type_name: module hierarchy to the struct type
# 
#     """
#     try:
#         out, err = subprocess.Popen(["/home/firas/cyclone/cyclonedds/bld/src/idlc/dds_idlc", idl_path], stdout=subprocess.PIPE).communicate()
#     except TimeoutExpired:
#         print(err)
        


# def get_dds_classes_from_idl(idl_path, type_name):
#     """Create topic data class and DDS type support class
#     from the given IDL file source.
# 
#     :type idl_path: string
#     :param idl_path: path to IDL file
# 
#     :type type_name: string
#     :param type_name: struct module (e.g., test::basic::my_struct)
# 
#     :rtype: GeneratedClassInfo
#     :return: GeneratedClassInfo
# 
#     Examples:
#         gen_info = dds_class("sample.idl", "basic::test::Type1", "long_1")
# 
#     """
#     topictype = _get_dds_descriptor_from_idl(idl_path, type_name)
    
    #descriptor = topictype.findtext('descriptor')
    #keys = topictype.findtext('keys')
    #To Do : check output for error

    # return _get_dds_classes_from_descriptor(descriptor, type_name, keys)

class TopicTest (unittest.TestCase):
    def setUp(self):
        self.helloworld_lib = CDLL(helloworld_lib_path)
        
        self.rt = Runtime.get_runtime()
        self.dp = Participant(0)
        self.name = "topic_name"
        self.type_support = self.get_hello_world_simple_value_type_support()
        self.topic = Topic (self.dp, self.name, self.type_support , None, None)
    
    def get_hello_world_key_value_type_support(self):
        return self.helloworld_lib.HelloWorldDataMsg_keys

    def get_hello_world_simple_value_type_support(self):
        return self.helloworld_lib.HelloWorldData_Msg_desc
    
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
        # get_name = self.topic.dds_get_name(result_topic_name)
        get_name = self.topic.name
        self.assertEqual(get_name, self.topic.name, "Wrong topic name returned from property name")
    
    def test_get_type_name(self):
        expected_topic_name = "HelloWorldData::Msg"
        # get_name = self.topic.dds_get_name(result_topic_name)
        get_name = self.topic.type_name()
        self.assertEqual(get_name, expected_topic_name, "Wrong topic type name returned ")

        
if __name__ == "__main__":
    unittest.main() # run all tests
