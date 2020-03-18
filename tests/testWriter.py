import unittest

__author__ = 'ADlink Technology'

from cdds import *

import os, sys

from idl_parser import parser

parser_ = parser.IDLParser()

from idl_parser import parser
import cdds.py_dds_utils as utils

import time



class DataWriterTest (unittest.TestCase):
    def setUp(self):
        self.helloworld_lib = CDLL(helloworld_lib_path)
        
        self.rt = Runtime.get_runtime()
        self.dp = Participant(0)
        self.pub = Publisher(self.dp)
        self.sub = Subscriber(self.dp)
        
        topic_name = "HelloWorldData_Msg"
        type_support = self.get_hello_world_simple_value_type_support()
        
        self.topic = self.dp.create_topic(topic_name, type_support)
        
        self.writer = Writer(self.pub, self.topic, [Reliable(), KeepLastHistory(10)])
        self.reader = Reader(self.sub, self.topic,  [Reliable(), KeepLastHistory(10)])
        
    def test_init_writer(self):
        self.assertIsNotNone (self.writer, "Initializing the data_writer failed")
        self.assertIsInstance(self.writer, Writer)
    
    def get_hello_world_key_value_type_support(self):
        return self.helloworld_lib.HelloWorldDataMsg_keys

    def get_hello_world_simple_value_type_support(self):
        return self.helloworld_lib.HelloWorldData_Msg_desc
        
    def test_write(self):
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        with open(idl_path, 'r') as idlf:
            contents = idlf.read()
            
            global_module = parser_.load( contents)
            my_module = global_module.module_by_name('HelloWorldData')
            
            MsgSeq = my_module.struct_by_name('Msg')
        
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        
        newMsg = HelloWorldData_Msg(userID = 23, message = "Other message")
        print("Writer >> Begin writeing data")
        rc = self.writer.write(newMsg)
        print("Writer >> Writing data completed")
        time.sleep(5)
        read_sample = False
        print('reader>> begin read loop!')
        while(not read_sample) :
            time.sleep(1)
            samples = self.reader.read(all_samples())
            if samples is not None:
                
                cnt = 0
                samples_as_list = list(samples)

                for s in samples_as_list:
                    if s[1].valid_data:
                        sam = s[0]
                        sam_new = cast(c_void_p(sam), POINTER(DDSKeyValue))
                        if sam_new.contents.value is not None:
                            v = sam_new.contents.value.decode(encoding='UTF-8')
                            
                            read_sample = True
                            try:
                                value = jsonpickle.decode(v)
                                val_ = (HelloWorldData_Msg)(**value)
                                print('********************************************************')
                                print('******************Written data was**********************')
                                print('val = {}'.format(val_))
                                print('val_.userID {}'.format(val_.userID))
                                print('val_.message {}'.format( val_.message))
                                print('******************Read data was*************************')
                                print("newMsg = {}".format(newMsg))
                                print('newMsg.userID {}'.format( newMsg.userID))
                                print('newMsg.message{}'.format( newMsg.message))
                                print('********************************************************')

                                self.assertEqual(val_, newMsg)
                            except:
                                raise Exception ("Invalid data received")
                                

    

if __name__ == "__main__":
    unittest.main() # run all tests
