
from cdds import *

import os, sys

from idl_parser import parser
from time import sleep

parser_ = parser.IDLParser()

from idl_parser import parser
import cdds.py_dds_utils as utils

import time

class TopicListener(Listener):
    def __init__(self):
        super(TopicListener, self).__init__()

    def on_inconsistent_topic(self, status):
        print("Inconsistent topic is found")

class DataAvailableListener(Listener):
    def __init__(self):
        super(DataAvailableListener, self).__init__()

    def on_subscription_matched(self, reader, status):
        OKCYAN = '\033[36m'
        ENDC = '\033[0m'
        print (f"{OKCYAN}Subscription matched{ENDC}")
        status = reader.subscription_matched_status()
        print(f"{OKCYAN}status.total_count{ENDC}", status.total_count)
        print(f"{OKCYAN}status.total_count_change{ENDC}", status.total_count_change)
        print(f"{OKCYAN}status.current_count{ENDC}", status.current_count)
        print(f"{OKCYAN}status.current_count_change{ENDC}", status.current_count_change)
        print(f"{OKCYAN}status.last_publication_handle{ENDC}", status.last_publication_handle)


class Sub():
    def __init__(self):
        self.helloworld_lib = CDLL(helloworld_lib_path)

        self.rt = Runtime.get_runtime()
        self.dp = Participant(0)
        self.pub = Publisher(self.dp)
        self.sub = Subscriber(self.dp, None, SubscriberListener())

        topic_name = "HelloWorldData_Msg"
        #type_support = self.get_hello_world_simple_value_type_support()
        type_support = self.rt.get_key_value_type_support()

        self.topic = self.dp.create_topic(topic_name, type_support, None, TopicListener())

        self.reader = Reader(self.sub, self.topic,  [Reliable(), KeepLastHistory(5), Deadline(dds_secs(10)), ResourceLimit(4, 10, 5)], DataAvailableListener())

if __name__ == "__main__":
    sub = Sub()
    print("Starting main loop of the reader, waiting for data")
    while True:
        time.sleep(1)
