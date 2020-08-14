import unittest

from cdds import *

from idl_parser import parser

import cdds.py_dds_utils as utils

import time

__author__ = 'ADlink Technology'
parser_ = parser.IDLParser()


class DataWriterTest(unittest.TestCase):
    def setUp(self):
        self.helloworld_lib = CDLL(helloworld_lib_path)

        self.rt = Runtime.get_runtime()
        self.dp = Participant(0)
        self.pub = Publisher(self.dp)
        self.sub = Subscriber(self.dp)

        topic_name = "HelloWorldData_Msg"
        # type_support = self.get_hello_world_simple_value_type_support()
        type_support = self.rt.get_key_value_type_support()

        self.topic = self.dp.create_topic(topic_name, type_support)

        self.writer = Writer(self.pub, self.topic, [Reliable(), KeepLastHistory(10)])
        self.reader = Reader(self.sub, self.topic, [Reliable(), KeepLastHistory(10)])

    def test_init_writer(self):
        self.assertIsNotNone(self.writer, "Initializing the data_writer failed")
        self.assertIsInstance(self.writer, Writer)

    def get_hello_world_key_value_type_support(self):
        # return self.helloworld_lib.HelloWorldDataMsg_keys
        return self.writer.rt.get_key_value_type_support

    def get_hello_world_simple_value_type_support(self):
        return self.helloworld_lib.HelloWorldData_Msg_desc

    def test_write(self):
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'

        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className, idl_path)

        newMsg = HelloWorldData_Msg(userID=1, message="Other message")
        print("Writer >> Begin writeing data")
        rc = self.writer.write(newMsg)
        self.assertEqual(rc, 0, "Error occurred during write operation")
        print("Writer >> Writing data completed")
        time.sleep(5)
        sample_read = False
        cnt_samples = 0
        print('reader>> begin read loop!')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = self.reader.read()
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data and x[0] and x[0] != '', samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            if sam is not None:
                                cnt_samples += 1
                                print("sam =", sam)
                                val_ = (HelloWorldData_Msg)(**sam)
                                print('********************************************************')
                                print('******************Read data was**********************')
                                print('val = {}'.format(val_))
                                print('val_.userID {}'.format(val_.userID))
                                print('val_.message {}'.format(val_.message))

                                self.assertTrue(val_.userID is newMsg.userID, "Read message has an invalid key {0}".format(val_.userID))
            except:
                print("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])

    def test_writedispose(self):
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'

        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className, idl_path)

        for i in range(10, 20):
            newMsg = HelloWorldData_Msg(userID=i, message="Other message {0}".format(i))
            print("Writer >> Begin writeing data {0}".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation did not succeed")
            time.sleep(1)

        time.sleep(5)
        print("Writer >> Begin writeing data")
        rc = self.writer.write(newMsg)
        print("Writer >> Writing data completed")
        time.sleep(5)
        sample_read = False
        cnt_samples = 0
        print('reader>> begin read loop!')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = self.reader.read()
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data and x[0] and x[0] != '', samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            if sam is not None:
                                cnt_samples += 1
                                val_ = (HelloWorldData_Msg)(**sam)
                                print('********************************************************')
                                print('******************Read data was**********************')
                                print('val = {}'.format(val_))
                                print('val_.userID {}'.format(val_.userID))
                                print('val_.message {}'.format(val_.message))
                                print("s[1].instance_handle = ", s[1].instance_handle)
                                self.assertTrue(val_.userID in range(10, 20), "Read message has an invalid key {0}".format(val_.userID))
            except:
                print("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])
            sample_to_dispose = HelloWorldData_Msg(userID=13, message="Other message 13")
            rc = self.writer.write_dispose(sample_to_dispose)
            self.assertEqual(rc, 0, "dispose instance failed")
            time.sleep(5)
            print("Sample disposed")
            sample_read = False
            cnt_samples = 0
            mask = DDS_ANY_SAMPLE_STATE | DDS_ANY_VIEW_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE
            print('reader>> begin read loop!')
            print("cnt_samples ", cnt_samples)
            while(not sample_read):
                time.sleep(1)
                try:
                    samples = self.reader.read_mask(mask)
                    print("here 1")
                    if samples is not None:
                        print("here 2")
                        samples_as_list = list(samples)
                        print("samples ", samples)
                        print("samples_as_list ", samples_as_list)
                        #  for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        for s in list(samples_as_list):
                            print("here 3")
                            if s[0] is not None and s[1].valid_data:
                                print("here 4")
                                sample_read = True
                                sam = s[0]
                                if sam is not None:
                                    cnt_samples += 1
                                    val_ = (HelloWorldData_Msg)(**sam)
                                    print('********************************************************')
                                    print('******************Read data was**********************')
                                    print('val = {}'.format(val_))
                                    print('val_.userID {}'.format(val_.userID))
                                    print('val_.message {}'.format(val_.message))
                                    print("s[1].instance_handle = ", s[1].instance_handle)
                                    print("s[1].instance_state = ", s[1].instance_state)
                                    if(val_.userID != 13):
                                        self.assertEqual(s[1].instance_state, DDS_ALIVE_INSTANCE_STATE, "Read message has an invalid instacne_state {0}".format(s[1].instance_state))
                                        self.assertEqual(s[1].sample_state, DDS_READ_SAMPLE_STATE, "Read samples does not have the good mask")
                                    else:
                                        self.assertEqual(s[1].instance_state, DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE, "Read message has an invalid instacne_state {0}".format(s[1].instance_state))
                                        # self.assertEqual(s[1].sample_state, DDS_NOT_READ_SAMPLE_STATE, "Read samples does not have the good mask")
                                self.assertTrue(val_.userID in range(10, 20), "Read message has an invalid key {0}".format(val_.userID))
                except:
                    print("Invalid data read")
                    raise Exception("Unexpected error:", sys.exc_info()[0])

    def test_dispose(self):
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className, idl_path)
        for i in range(30, 40):
            newMsg = HelloWorldData_Msg(userID=i, message="Other message {0}".format(i))
            print("Writer >> Begin writeing data {0}".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation did not succeed")
            time.sleep(1)
        time.sleep(5)
        print("Writer >> Begin writeing data")
        rc = self.writer.write(newMsg)
        print("Writer >> Writing data completed")
        time.sleep(5)
        sample_read = False
        cnt_samples = 0
        print('reader>> begin read loop!')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = self.reader.read()
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data and x[0] and x[0] != '', samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            if sam is not None:
                                cnt_samples += 1

                                val_ = (HelloWorldData_Msg)(**sam)
                                print('********************************************************')
                                print('******************Read data was**********************')
                                print('val = {}'.format(val_))
                                print('val_.userID {}'.format(val_.userID))
                                print('val_.message {}'.format(val_.message))
                                print("s[1].instance_handle = ", s[1].instance_handle)
                                self.assertTrue(val_.userID in range(30, 40), "Read message has an invalid key {0}".format(val_.userID))
            except:
                print("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])
            sample_to_dispose = HelloWorldData_Msg(userID=33, message="Other message 33")
            rc = self.writer.write_dispose(sample_to_dispose)
            self.assertEqual(rc, 0, "dispose instance failed")
            time.sleep(5)
            print("Sample disposed")
            sample_read = False
            cnt_samples = 0
            print('reader>> begin read loop!')
            print("cnt_samples ", cnt_samples)
            while(not sample_read):
                time.sleep(1)
                try:
                    #  samples = self.reader.read_mask(mask)
                    samples = self.reader.read()
                    print("here 1")
                    if samples is not None:
                        print("here 2")
                        samples_as_list = list(samples)
                        print("samples ", samples)
                        print("samples_as_list ", samples_as_list)
                        #  for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        for s in list(samples_as_list):
                            print("here 3")
                            if s[0] is not None and s[1].valid_data:
                                print("here 4")
                                sample_read = True
                                sam = s[0]
                                if sam is not None:
                                    cnt_samples += 1
                                    val_ = (HelloWorldData_Msg)(**sam)
                                    print('********************************************************')
                                    print('******************Read data was**********************')
                                    print('val = {}'.format(val_))
                                    print('val_.userID {}'.format(val_.userID))
                                    print('val_.message {}'.format(val_.message))
                                    print("s[1].instance_handle = ", s[1].instance_handle)
                                    print("s[1].instance_state = ", s[1].instance_state)
                                    if(val_.userID != 33):
                                        self.assertEqual(s[1].instance_state, DDS_ALIVE_INSTANCE_STATE, "Read message with userID={0} has an invalid instacne_state {1}".format(val_.userID, s[1].instance_state))
                                        self.assertEqual(s[1].sample_state, DDS_READ_SAMPLE_STATE, "Read samples does not have the good mask, val_userID={0}".format(val_.userID))
                                    else:
                                        self.assertEqual(s[1].instance_state, DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE, "Read message with userID={0} has an invalid instacne_state {1}".format(val_.userID, s[1].instance_state))
                                        #  self.assertEqual(s[1].sample_state, DDS_NOT_READ_SAMPLE_STATE, "Read samples does not have the good mask, val_userID={0}".format(val_.userID))
                                self.assertTrue(val_.userID in range(30, 40), "Read message has an invalid key {0}".format(val_.userID))
                except:
                    print("Invalid data read")
                    raise Exception("Unexpected error:", sys.exc_info()[0])


if __name__ == "__main__":
    unittest.main()  # run all tests
