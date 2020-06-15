
from cdds import *

import os, sys

from idl_parser import parser
from time import sleep

parser_ = parser.IDLParser()

from idl_parser import parser
import cdds.py_dds_utils as utils

import time

class DataAvailableListener(Listener):
    def __init__(self):
        super(DataAvailableListener, self).__init__()


    def on_data_available(self, reader):

        print("data available listener called")

        print("Begin read available data")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)

        cnt_samples = 0
        sample_read = False

        try:
            samples = reader.take()
            if samples is not None:
                samples_as_list = list(samples)
                for s in list(filter( lambda x: x[1].valid_data, samples_as_list)):
                    if s[0] is not None and s[1].valid_data:
                        sample_read = True
                        sam = s[0]
                        cnt_samples += 1

                        val_ = (HelloWorldData_Msg)(**sam)
                        print('********************************************************')
                        print('******************Read data was**********************')
                        print('val = {}'.format(val_))
                        print('val_.userID {}'.format(val_.userID))
                        print('val_.message {}'.format( val_.message))
                        print ("s[1].instance_handle ", s[1].instance_handle)

                        time.sleep(2)

        except:
            print("Error occurred while trying to handle data available")
            raise Exception("Unexpected error:", sys.exc_info()[0])



class Sub():
    def __init__(self):
        self.helloworld_lib = CDLL(helloworld_lib_path)

        self.rt = Runtime.get_runtime()
        self.dp = Participant(0)
        self.pub = Publisher(self.dp)
        self.sub = Subscriber(self.dp)

        topic_name = "HelloWorldData_Msg"
        #type_support = self.get_hello_world_simple_value_type_support()
        type_support = self.rt.get_key_value_type_support()

        self.topic = self.dp.create_topic(topic_name, type_support)

        self.reader = Reader(self.sub, self.topic,  [Reliable(), KeepLastHistory(5), Deadline(dds_secs(5)), ResourceLimit(-1, -1, -1)], DataAvailableListener())

if __name__ == "__main__":
    sub = Sub()
    print("Starting main loop of the reader, waiting for data")
    while True:
        time.sleep(1)
