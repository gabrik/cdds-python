
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

    def on_liveliness_changed(self, reader, status):
        print ("Liveliness_changed")
        OKGREEN = '\033[32m'
        ENDC = '\033[0m'
        status = reader.liveliness_changed_status()
        print(f"{OKGREEN}status.alive_count", status.alive_count)
        print(f"{OKGREEN}status.not_alive_count{ENDC}", status.not_alive_count)
        print(f"{OKGREEN}status.alive_count_change{ENDC}", status.alive_count_change)
        print(f"{OKGREEN}status.not_alive_count_change{ENDC}", status.not_alive_count_change)
        print(f"{OKGREEN}status.last_publication_handle{ENDC}", status.last_publication_handle)

    def on_requested_deadline_missed(self, reader, status):
        OKBLUE = '\033[94m'
        ENDC = '\033[0m'
        print ("requested deadline missed")
        s = reader.requested_deadline_missed_status()
        print(f"{OKBLUE}status.total_count{ENDC}", s.total_count)
        print(f"{OKBLUE}status.total_count_change{ENDC}", s.total_count_change)
        print(f"{OKBLUE}status.last_instance_handle{ENDC}", s.last_instance_handle)


    def on_sample_rejected (self, reader, status):
        OKGREEN = '\033[32m'
        ENDC = '\033[0m'
        print ("sample rejected")
        s = reader.get_rejected_sample_status()
        print(f"{OKGREEN}status.total_count{ENDC}", s.total_count)
        print(f"{OKGREEN}status.total_count_change{ENDC}", s.total_count_change)
        print(f"{OKGREEN}status.last_reason{ENDC}", s.last_reason)
        print(f"{OKGREEN}status.last_instance_handle{ENDC}", s.last_instance_handle)
        time.sleep(1)

    def on_sample_lost (self, reader, status):
        OKYELLOW = '\033[33m'
        ENDC = '\033[0m'
        print ("sample lost")
        s = reader.get_lost_sample_status()
        print(f"{OKYELLOW}status.total_count{ENDC}", s.total_count)
        print(f"{OKYELLOW}status.total_count_change{ENDC}", s.total_count_change)

    def requested_incompatible_qos_status(self, writer, status):
        print ("offered incompatible QoS policy")
        OKGREEN = '\033[32m'
        ENDC = '\033[0m'
        status = writer.requested_incompatible_qos_status()
        print(f"{OKGREEN}status.total_count", status.total_count)
        print(f"{OKGREEN}status.total_count_change{ENDC}", status.total_count_change)
        print(f"{OKGREEN}status.last_policy_id {ENDC}", status.last_policy_id)


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

        self.reader = Reader(self.sub, self.topic,  [Reliable(), KeepLastHistory(5), Deadline(dds_secs(10)), ResourceLimit(4, 10, 5)], DataAvailableListener())

if __name__ == "__main__":
    sub = Sub()
    print("Starting main loop of the reader, waiting for data")
    while True:
        time.sleep(1)
