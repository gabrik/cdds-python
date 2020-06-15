
from cdds import *

import os, sys

from idl_parser import parser

parser_ = parser.IDLParser()

from idl_parser import parser
import cdds.py_dds_utils as utils

import time


class WriterListener(Listener):
    def __init__(self):
        super(WriterListener, self).__init__()

    def on_offered_deadline_missed(self, writer, status):
        OKBLUE = '\033[94m'
        ENDC = '\033[0m'
        print ("offered deadline missed")
        s = writer.offered_deadline_missed_status()
        print(f"{OKBLUE}status.total_count{ENDC}", s.total_count)
        print(f"{OKBLUE}status.total_count_change{ENDC}", s.total_count_change)
        print(f"{OKBLUE}status.last_instance_handle{ENDC}", s.last_instance_handle)


    def on_publication_matched(self, writer, status):
        OKCYAN = '\033[36m'
        ENDC = '\033[0m'
        print (f"{OKCYAN}Publication matched{ENDC}")
        status = writer.publication_matched_status()
        print(f"{OKCYAN}status.total_count{ENDC}", status.total_count)
        print(f"{OKCYAN}status.total_count_change{ENDC}", status.total_count_change)
        print(f"{OKCYAN}status.current_count{ENDC}", status.current_count)
        print(f"{OKCYAN}status.current_count_change{ENDC}", status.current_count_change)
        print(f"{OKCYAN}status.last_subscription_handle{ENDC}", status.last_subscription_handle)

    def on_liveliness_lost(self, writer, status):
        print ("Liveliness_lost")
        OKGREEN = '\033[32m'
        ENDC = '\033[0m'
        status = reader.liveliness_lost_status()
        print(f"{OKGREEN}status.total_count", status.total_count)
        print(f"{OKGREEN}status.total_count_change{ENDC}", status.total_count_change)

    def offered_incompatible_qos_status(self, writer, status):
        print ("offered incompatible QoS policy")
        OKGREEN = '\033[32m'
        ENDC = '\033[0m'
        status = writer.offered_incompatible_qos_status()
        print(f"{OKGREEN}status.total_count", status.total_count)
        print(f"{OKGREEN}status.total_count_change{ENDC}", status.total_count_change)
        print(f"{OKGREEN}status.last_policy_id {ENDC}", status.last_policy_id)



class pub():
    def __init__(self):
        self.helloworld_lib = CDLL(helloworld_lib_path)

        self.rt = Runtime.get_runtime()
        self.dp = Participant(0)
        self.pub = Publisher(self.dp)

        topic_name = "HelloWorldData_Msg"
        #type_support = self.get_hello_world_simple_value_type_support()
        type_support = self.rt.get_key_value_type_support()

        self.topic = self.dp.create_topic(topic_name, type_support)

        self.writer = Writer(self.pub, self.topic, [Reliable(), KeepLastHistory(10), Deadline(dds_secs(5)), ResourceLimit(-1, -1, -1)], WriterListener())


    def write(self):
        print("begin creating writer")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        print("Writer >> Begin writing data")
        cnt = 1
        while True:
            newMsg = HelloWorldData_Msg(userID = (cnt % 5), message = "Message {0}".format(cnt))

            rc = self.writer.write(newMsg)

            print(" message written {0}".format(newMsg))

            cnt += 1

            time.sleep(1)
            if cnt % 5 == 0 :
                time.sleep(8)

if __name__ == "__main__":
    #inccomp_pub = IncompPub()

    # inccomp_pub.writer.delete()

    publisher = pub()
    time.sleep(2)
    publisher.write()
