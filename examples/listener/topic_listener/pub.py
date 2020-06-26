
from cdds import *

import os, sys

from idl_parser import parser

parser_ = parser.IDLParser()

from idl_parser import parser
import cdds.py_dds_utils as utils

import time

class TopicListener(Listener):
    def __init__(self):
        super(TopicListener, self).__init__()

    def on_inconsistent_topic(self, status):
        print("Inconsistent topic is found")

class pub():
    def __init__(self):
        self.helloworld_lib = CDLL(helloworld_lib_path)
        
        self.rt = Runtime.get_runtime()
        self.dp = Participant(0)
        self.pub = Publisher(self.dp)
        
        topic_name = "HelloWorldData_Msg"
        #type_support = self.get_hello_world_simple_value_type_support()
        type_support = self.rt.get_key_value_type_support()
        
        self.topic = self.dp.create_topic(topic_name, type_suppor, None, TopicListener())
        
        self.writer = Writer(self.pub, self.topic, [Reliable(), KeepLastHistory(5), Deadline(dds_secs(10)), ResourceLimit(4, 10, 5)])
        
    
    def write(self):
        print("Begin test_read")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        print("Writer >> Begin writing data")
        cnt = 1
        while True:
            newMsg = HelloWorldData_Msg(userID = ((cnt % 6) +1), message = "Message {0}".format(cnt))
            
            rc = self.writer.write(newMsg)
            
            print(" message written {0}".format(newMsg))
            
            cnt += 1
            
            time.sleep(1)
            
if __name__ == "__main__":
    inccomp_pub = IncompPub()
    
    inccomp_pub.writer.delete()
    
    publisher = pub()
    time.sleep(2)
    publisher.write()