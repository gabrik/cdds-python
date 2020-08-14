import unittest
from ctypes import c_bool, c_void_p

import jsonpickle

from cdds import *

import sys

from idl_parser import parser

import cdds.py_dds_utils as utils

import time

__author__ = 'ADlink Technology'

parser_ = parser.IDLParser()


class QueryConditionTest(unittest.TestCase):
    def setUp(self):
        self.helloworld_lib = CDLL(helloworld_lib_path)
        self.rt = Runtime.get_runtime()
        self.dp = Participant(0)
        self.pub = Publisher(self.dp)
        self.sub = Subscriber(self.dp)

        topic_name = "HelloWorldData_Msg"
        type_support = self.rt.get_key_value_type_support()
        self.topic = self.dp.create_topic(topic_name, type_support)

        self.writer = Writer(self.pub, self.topic, [Reliable(), KeepLastHistory(10)])
        self.reader = Reader(self.sub, self.topic, [Reliable(), KeepLastHistory(10)])

        MYFUNCTYPE = CFUNCTYPE(c_bool, c_void_p)
        self.my_c_func = MYFUNCTYPE(self.filter)
        self.message_c_func = MYFUNCTYPE(self.filter_message)

    def tearDown(self):
        self.rt.close()

    def test_init_QueryCondition(self):
        mask = DDS_ANY_SAMPLE_STATE | DDS_ANY_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        cond = QueryCondition(self.reader, mask, self.my_c_func)
        self.assertIsNotNone(cond, "QueryCondition creation failed")
        self.assertIsInstance(cond, QueryCondition, "Query condition is not of the good type")

    def test_get_mask(self):
        mask = DDS_ANY_SAMPLE_STATE | DDS_ANY_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        cond = QueryCondition(self.reader, mask, self.my_c_func)
        res_mask = cond.get_mask()
        self.assertIsNotNone(res_mask, "get mask returned a not valid object")
        self.assertEqual(res_mask.value, c_uint(mask).value, "get_msk retuened a wrong_value {0} != {1}".format(res_mask, mask))
        mask = DDS_NOT_READ_SAMPLE_STATE | DDS_NEW_VIEW_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE
        cond = QueryCondition(self.reader, mask, self.my_c_func)
        res_mask = cond.get_mask()
        self.assertIsNotNone(res_mask, "get mask returned a not valid object")
        self.assertEqual(res_mask.value, c_uint(mask).value, "get_msk retuened a wrong_value {0} != {1}".format(res_mask, mask))

    def test_get_reader(self):
        mask = DDS_ANY_SAMPLE_STATE | DDS_ANY_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        cond = QueryCondition(self.reader, mask, self.my_c_func)
        handle = cond.get_reader_handle()
        self.assertIsNotNone(handle, " get_reader_handle returned an invalid handle")
        self.assertEqual(handle, self.reader.handle, " get_reader_handle returned wrong handle")

    def test_read(self):
        print("Begin test_read")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className, idl_path)
        for i in range(0, 5):
            newMsg = HelloWorldData_Msg(userID=i, message="Other message {0}".format(i))
            print("Writer >> Begin writeing data")
            rc = self.writer.write(newMsg)

        time.sleep(5)
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = self.reader.read()
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1
                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))
                            self.assertTrue(val_.userID in range(0, 5), "Read message has an invalid key {0}".format(val_.userID))
            except:
                print("Invalid data read")
        self.assertEqual(cnt_samples, 5, "read samples are not as expected")
        mask = DDS_READ_SAMPLE_STATE | DDS_ANY_VIEW_STATE | DDS_ALIVE_INSTANCE_STATE
        cond = QueryCondition(self.reader, mask, self.my_c_func)

        mask2 = DDS_NOT_READ_SAMPLE_STATE | DDS_ANY_VIEW_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE
        cond2 = QueryCondition(self.reader, mask2, self.message_c_func)

        msg = HelloWorldData_Msg(userID=1, message="new message ")
        print("Writer >> Begin writeing data")
        self.writer.write_dispose(msg)
        time.sleep(5)

        print('query_condition >> begin read loop!')
        print('mask = DDS_READ_SAMPLE_STATE | DDS_ANY_VIEW_STATE | DDS_ALIVE_INSTANCE_STATE')
        print('Cond userID % 2 = 0')
        cnt_samples = 0
        sample_read = False
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond.read()
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1

                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))

                            self.assertIn(val_.userID, range(0, 5), "Read message has an invalid key {0}".format(val_.userID))
            except:
                print("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])

        for i in range(0, 3):
            newMsg = HelloWorldData_Msg(userID=i, message="new message {0}".format(i))
            print("Writer >> Begin writeing data")
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Error during write operation")
        msg = HelloWorldData_Msg(userID=3, message="new message ")
        print("Writer >> Begin writeing data")
        self.writer.write_dispose(msg)
        time.sleep(5)

        print('query_condition >> begin read loop!')
        print('mask2 = DDS_NOT_READ_SAMPLE_STATE | DDS_ANY_VIEW_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE')
        print('Cond message.find("new")!= -1 ')
        cnt_samples = 0
        sample_read = False
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond2.read()
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1
                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))
                            self.assertTrue(val_.userID == 3, "Read message has an invalid key {0}".format(val_.userID))
            except:
                print("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])
        self.assertEqual(cnt_samples, 1, "read_condition: read samples are not as expected")

    def test_read_n(self):
        print("Begin test_read_n")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className, idl_path)

        for i in range(10, 15):
            newMsg = HelloWorldData_Msg(userID=i, message="new message {0}".format(i))
            print("Writer >> Begin writeing data {0}".format(newMsg))
            rc = self.writer.write(newMsg)
            print("rc = ", rc)
            self.assertEqual(rc, 0, "Write operation did not succeed")
            time.sleep(1)

        time.sleep(5)

        mask = DDS_NOT_READ_SAMPLE_STATE | DDS_ANY_VIEW_STATE | DDS_ALIVE_INSTANCE_STATE
        cond = QueryCondition(self.reader, mask, self.my_c_func)

        sample_read = False
        print('cond >> begin read loop!')
        cnt_samples = 0
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond.read_n(2)
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s.status.valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1
                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))
                            self.assertTrue(val_.userID in {10, 12}, "Read message has an invalid key {0}".format(val_.userID))
            except:
                print("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])
            self.assertEqual(cnt_samples, 2, "Different number read by read_n(2)")
            cond2 = QueryCondition(self.reader, mask, self.message_c_func)
            sample_read = False
            print('cond >> begin read loop!')
            cnt_samples = 0
            while(not sample_read):
                time.sleep(1)
                try:
                    samples = cond2.read_n(3)
                    if samples is not None:
                        samples_as_list = list(samples)
                        for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                            if s[0] is not None and s.status.valid_data:
                                sample_read = True
                                sam = s[0]
                                cnt_samples += 1
                                val_ = (HelloWorldData_Msg)(**sam)
                                print('********************************************************')
                                print('******************Read data was**********************')
                                print('val = {}'.format(val_))
                                print('val_.userID {}'.format(val_.userID))
                                print('val_.message {}'.format(val_.message))
                                self.assertTrue(val_.userID in {11, 13, 14}, "Read message has an invalid key {0}".format(val_.userID))
                except:
                    print("Invalid data read")
                    raise Exception("Unexpected error:", sys.exc_info()[0])
                self.assertEqual(cnt_samples, 3, "Different number read by read_n(2)")

    def test_read_mask(self):
        print("Begin test_read_mask")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className, idl_path)

        print("Writer >> Begin writeing data")

        for i in range(30, 35):
            newMsg = HelloWorldData_Msg(userID=i, message="Other message {0}".format(i))
            print("written sample {0} ".format(newMsg))
            rc = self.writer.write(newMsg)

        time.sleep(5)

        mask = DDS_NOT_READ_SAMPLE_STATE | DDS_NEW_VIEW_STATE | DDS_ALIVE_INSTANCE_STATE
        cond = QueryCondition(self.reader, mask, self.my_c_func)

        read_mask = DDS_NOT_READ_SAMPLE_STATE | DDS_NEW_VIEW_STATE | DDS_ANY_INSTANCE_STATE
        print('cond >> begin read loop!(read_mask = {0}, mask = {1})'.format(read_mask, mask))
        cnt_samples = 0
        sample_read = False
        print('cond >> begin read loop!')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond.read_mask(read_mask)
                if samples is not None:
                    print("samples is not none")
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        print("scanning sample_list")
                        if s[0] is not None and s[1].valid_data:
                            print("valid sample")
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1
                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))
                            print("s[1].view_state=", s[1].view_state)
                            print("s[1].instance_state=", s[1].instance_state)
                            print("s[1].sample_state=", s[1].sample_state)
                            self.assertTrue(val_.userID in range(30, 35), "unexpected message read")
                            self.assertEqual(s[1].sample_state, DDS_NOT_READ_SAMPLE_STATE, "Read samples does not have the good mask")
                            self.assertEqual(s[1].instance_state, DDS_ALIVE_INSTANCE_STATE, "Read samples does not have the expected instance_state, userID={0}".format(val_.userID))
                            self.assertEqual(s[1].view_state, DDS_NEW_VIEW_STATE, "Read samples does not have the expected view_state, userID={0}".format(val_.userID))
            except:
                raise Exception("Invalid data received")
        self.assertEqual(cnt_samples, 3, "Wrong number of samples read")

        print("Test read with mask DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE ")

        for i in range(30, 40):
            newMsg = HelloWorldData_Msg(userID=i, message="Other message {0}".format(i))
            print("written sample {0} ".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Error while write operation")

        msg = HelloWorldData_Msg(userID=32, message="new message to dispose 32")
        print("Writer >> Begin writing dispose data")
        self.writer.write_dispose(msg)

        msg = HelloWorldData_Msg(userID=37, message="new message to dispose 35")
        print("Writer >> Begin writing dispose data")

        self.writer.write_dispose(msg)
        time.sleep(5)

        # All read samples will have sample_state = not_read,
        # and will have view_state = DDS_NEW_VIEW_STATE
        # and instance_state = DDS_ALIVE_INSTANCE_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE
        read_mask = DDS_NOT_READ_SAMPLE_STATE | DDS_NEW_VIEW_STATE | DDS_ALIVE_INSTANCE_STATE
        cnt_samples = 0
        sample_read = False
        print('cond >> begin read loop!(read_mask = {0}, mask = {1})'.format(read_mask, mask))
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond.read_mask(read_mask)
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1
                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))
                            self.assertTrue(val_.userID in range(30, 40), "unexpected message read val_.userID={0}".format(val_.userID))
                            self.assertTrue(s[1].sample_state | DDS_NOT_READ_SAMPLE_STATE, "sample_state is not correct")
                            self.assertEqual(s[1].instance_state, DDS_ALIVE_INSTANCE_STATE, "Read samples does not have the expected instance_state")
                            self.assertEqual(s[1].view_state, DDS_NEW_VIEW_STATE, "ViewState is not correct")
            except:
                raise Exception("Invalid data received")

        self.assertEqual(cnt_samples, 2, "Wrong number of samples read")

    def test_read_instacne(self):
        print("Begin test_read_instance")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className, idl_path)

        mask = DDS_NOT_READ_SAMPLE_STATE | DDS_ANY_VIEW_STATE | DDS_ALIVE_INSTANCE_STATE
        cond = QueryCondition(self.reader, mask, self.my_c_func)

        for i in range(60, 65):
            newMsg = HelloWorldData_Msg(userID=i, message="Other message {0}".format(i))
            print("Writer >> Begin writeing data {0}".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation did not succeed")
            time.sleep(1)

        time.sleep(5)

        cnt_samples = 0
        sample_read = False
        print('cond>> begin read loop!')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond.read()
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1
                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))
                            print("s[1].instance_handle ", s[1].instance_handle)
                            self.assertTrue(val_.userID in {60, 62, 64}, "Read message has an invalid key {0}".format(val_.userID))

            except:
                print("Invalid data read")
        self.assertEqual(cnt_samples, 3, "Wrong numbe of samples read")
        data = newMsg
        print(">>>>>>>>>>>>>>>>>>>>>>>> data =", data)
        inst_hdl = cond.lookup_instance(data)

        print("inst_hdl = ", inst_hdl)

        for i in range(60, 70):
            newMsg = HelloWorldData_Msg(userID=i, message="second message {0}".format(i))
            print("Writer >> Begin writeing data {0}".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation did not succeed")
            time.sleep(1)

        self.assertIsNotNone(inst_hdl, "Instance handle is not valid a valid handle")
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read_instance loop!')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond.read_instance(inst_hdl)
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1

                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))

                            self.assertTrue(val_.userID is data.userID, "Read message has an invalid key {0}".format(val_.userID))
                            self.assertEqual(s[1].instance_handle, inst_hdl, "Instacne handle of read sample is not the same as the one found in lookup_instance")
                else:
                    print("No samples read")
            except:
                print("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])
        self.assertEqual(cnt_samples, 1, "read samples are not as expected")

    def test_take(self):
        print("Begin test_take")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className, idl_path)

        mask = DDS_NOT_READ_SAMPLE_STATE | DDS_NEW_VIEW_STATE | DDS_ALIVE_INSTANCE_STATE
        cond = QueryCondition(self.reader, mask, self.my_c_func)

        for i in range(100, 105):
            newMsg = HelloWorldData_Msg(userID=i, message="Other message {0}".format(i))
            print("Writer >> Begin writeing data {0}".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation did not succeed")
            time.sleep(1)

        time.sleep(5)
        cnt_samples = 0
        sample_read = False
        print('cond >> begin read loop!')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond.take()
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1

                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))

                            self.assertEqual(s[1].instance_state, DDS_ALIVE_INSTANCE_STATE, "Read samples does not have the expected instance_state")
                            self.assertTrue(s[1].sample_state | DDS_NOT_READ_SAMPLE_STATE, "sample_state is not correct")
                            self.assertTrue(s[1].view_state | DDS_NOT_NEW_VIEW_STATE, "ViewState is not correct")

                            self.assertTrue(val_.userID in {100, 102, 104}, "Read message has an invalid key {0}".format(val_.userID))
            except:
                print("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])

        self.assertEqual(cnt_samples, 3, "read samples are not as expected")
        for i in range(100, 110):
            newMsg = HelloWorldData_Msg(userID=i, message="Other message {0}".format(i))
            print("Writer >> Begin writeing data {0}".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation did not succeed")
            time.sleep(1)

        time.sleep(5)
        cnt_samples = 0
        sample_read = False
        print('cond >> begin read loop!')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond.take()
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1

                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))
                            self.assertTrue(val_.userID in {106, 108}, "Read message has an invalid key {0}".format(val_.userID))
                            self.assertEqual(s[1].instance_state, DDS_ALIVE_INSTANCE_STATE, "Read samples does not have the expected instance_state")
                            self.assertTrue(s[1].sample_state | DDS_NOT_READ_SAMPLE_STATE, "sample_state is not correct")
                            self.assertTrue(s[1].view_state | DDS_NEW_VIEW_STATE, "ViewState is not correct")
            except:
                print("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])

        self.assertEqual(cnt_samples, 2, "read samples are not as expected")

    def test_take_mask(self):
        print("Begin test_take_mask")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className, idl_path)
        print("Writer >> Begin writeing data")

        mask = DDS_NOT_READ_SAMPLE_STATE | DDS_NEW_VIEW_STATE | DDS_ALIVE_INSTANCE_STATE
        cond = QueryCondition(self.reader, mask, self.my_c_func)

        for i in range(120, 125):
            newMsg = HelloWorldData_Msg(userID=i, message="Other message {0}".format(i))
            print("written sample {0} ".format(newMsg))
            rc = self.writer.write(newMsg)

        time.sleep(5)

        take_mask = DDS_NOT_READ_SAMPLE_STATE | DDS_NEW_VIEW_STATE | DDS_ANY_INSTANCE_STATE
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond.take_mask(take_mask)
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1

                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))
            except:
                print("Error occured while trying to read data while testing read_mask")

        print("Writer >> Begin writeing data")
        for i in range(120, 130):
            newMsg = HelloWorldData_Msg(userID=i, message="new message {0}".format(i))
            print("written sample {0} ".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Error occurred while write operation, file: __FILE__ on line __LINE__")
        time.sleep(5)

        sample = HelloWorldData_Msg(userID=123, message="message to dispose")
        self.writer.write_dispose(sample)

        sample = HelloWorldData_Msg(userID=127, message="message to dispose")
        self.writer.write_dispose(sample)
        time.sleep(5)

        # mask used in take_mask is mask | take_mask
        take_mask = DDS_NOT_READ_SAMPLE_STATE | DDS_NEW_VIEW_STATE | DDS_ALIVE_INSTANCE_STATE

        cnt_samples = 0
        sample_read = False
        print('cond.take_mask >> begin read loop!')
        print('test take_mask(\"DDS_ANY_SAMPLE_STATE | DDS_ANY_VIEW_STATE| DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE\"')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond.take_mask(take_mask)
                if samples is not None:
                    print("samples is not none")
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        print("scanning sample_list")
                        if s[0] is not None and s[1].valid_data:
                            print("valid sample")
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1

                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))
                            print('s[1].sample_state = {0}'.format(s[1].sample_state))
                            print('s[1].instance_state {0}'.format(s[1].instance_state))

                            self.assertTrue(val_.userID in {126, 128}, "unexpected message read userID={0}".format(val_.userID))
                            self.assertEqual(s[1].sample_state, DDS_NOT_READ_SAMPLE_STATE, "Read samples does not have the good mask")
                            self.assertEqual(s[1].instance_state, DDS_ALIVE_INSTANCE_STATE, "Read samples does not have the expected instance_state, userID={0}".format(val_.userID))

            except:
                raise Exception("Invalid data received")
        self.assertEqual(cnt_samples, 2, "Wrong number of samples read")

        mask2 = DDS_NOT_READ_SAMPLE_STATE | DDS_ANY_VIEW_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE
        cond2 = QueryCondition(self.reader, mask2, self.message_c_func)

        # 3 samples are read, but one of them is disposed

        mask_take = DDS_READ_SAMPLE_STATE | DDS_NEW_VIEW_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE

        print("Test read with mask DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE ")
        print("mask2 = DDS_NOT_READ_SAMPLE_STATE | DDS_NEW_VIEW_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE")
        print('mask_take = DDS_READ_SAMPLE_STATE | DDS_NEW_VIEW_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE')

        cnt_samples = 0
        sample_read = False
        print('cond 2 >> begin read loop!')
        while(not sample_read):
            time.sleep(1)
            try:
                samples = cond2.take_mask(mask_take)
                if samples is not None:
                    samples_as_list = list(samples)
                    for s in list(filter(lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s[1].valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1
                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format(val_.message))

                            self.assertTrue(val_.userID in {123, 127}, "unexpected message read")
                            self.assertEqual(s[1].instance_state, DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE, "Read samples does not have the expected instance_state")
            except:
                raise Exception("Invalid data received")
        # All samplse are taken now, there is only the disposed samples with userId =113
        self.assertEqual(cnt_samples, 2, "Wrong number of samples read")

    def filter(self, s):
        sp = cast(c_void_p(s), POINTER(DDSKeyValue))
        result = False
        if(sp[0].value is not None and sp[0].key is not None):
            sam = jsonpickle.decode(sp[0].value.decode(encoding='UTF-8'))
            # val_ = (HelloWorldData_Msg)(**sam)
            key = sam['userID']
            result = (key > 0) and (key % 2 == 0)

        return result

    def filter_message(self, s):
        sp = cast(c_void_p(s), POINTER(DDSKeyValue))
        result = False
        if(sp[0].value is not None and sp[0].key is not None):
            sam = jsonpickle.decode(sp[0].value.decode(encoding='UTF-8'))
            # val_ = (HelloWorldData_Msg)(**sam)
            key = sam['message']
            result = (key.find('new') is not -1)
        return result


if __name__ == "__main__":
    unittest.main()  # run all tests
