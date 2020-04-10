import unittest

__author__ = 'ADlink Technology'

from cdds import *

import os, sys

from idl_parser import parser

parser_ = parser.IDLParser()

import cdds.py_dds_utils as utils

import time

class DataReaderTest (unittest.TestCase):
    def setUp(self):
        
        self.helloworld_lib = CDLL(helloworld_lib_path)
        
        self.rt = Runtime.get_runtime()
        self.dp = Participant(0)
        self.pub = Publisher(self.dp)
        self.sub = Subscriber(self.dp)
        
        topic_name = "HelloWorldData_Msg"
        #type_support = self.get_hello_world_simple_value_type_support()
        type_support = self.rt.get_key_value_type_support()
        
        self.topic = self.dp.create_topic(topic_name, type_support)
        
        self.writer = Writer(self.pub, self.topic, [Reliable(), KeepLastHistory(10)])
        self.reader = Reader(self.sub, self.topic,  [Reliable(), KeepLastHistory(10)])
    
    @unittest.skip("demonstrating skipping")
    def test_get_subscriber (self):
        print("Begin get_subscriber")
        entity = self.reader.get_subscriber()
        self.assertIsNotNone(entity, "get_subscriber returned a None")
        self.assertIsInstance(entity, sub.Subscriber, "get_subscriber returned an entity of a wrong type")
        self.assertEqual(entity, self.sub, "get_subscriber returned a wrong entity")
        
    @unittest.skip("demonstrating skipping") 
    def test_init_reader(self):
        print("Begin test_init_reader")
        self.assertIsNotNone (self.reader, "Initializing the data_writer failed")
        self.assertIsInstance(self.reader, Reader)
    
    @unittest.skip("demonstrating skipping")
    def test_read (self):
        print("Begin test_read")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        
        newMsg = HelloWorldData_Msg(userID = 1, message = "Other message")
        print("Writer >> Begin writeing data")
        rc = self.writer.write(newMsg)
        
        time.sleep(5)
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read()
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
                            
                            self.assertTrue(val_.userID is newMsg.userID, "Read message has an invalid key {0}".format(val_.userID))
            except:
                print ("Invalid data read")
                

        self.assertEqual(cnt_samples, 1, "read samples are not as expected")
     
    @unittest.skip("demonstrating skipping")
    def test_read_n (self):
        print("Begin test_read_n")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        
        for i in range(10, 15):
            newMsg = HelloWorldData_Msg(userID = i, message = "Other message {0}".format(i))
            print("Writer >> Begin writeing data {0}".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation did not succeed")
            time.sleep(1)
            
        time.sleep(5)
        
        sample_read = False
        print('reader>> begin read loop!')
        cnt_samples = 0
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read_n(2)
                if samples is not None:
                    samples_as_list = list(samples)    
                    for s in list(filter( lambda x: x[1].valid_data, samples_as_list)):
                        if s[0] is not None and s.status.valid_data:
                            sample_read = True
                            sam = s[0]
                            cnt_samples += 1
                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format( val_.message))
                            
                            self.assertTrue(val_.userID in range(10, 15), "Read message has an invalid key {0}".format(val_.userID))
            except:
                print ("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])
            self.assertEqual(cnt_samples, 2, "Diferent number read by read_n(2) b")
    
    @unittest.skip("demonstrating skipping")
    def test_read_mask (self):
        print("Begin test_read_mask")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        
        print("Writer >> Begin writeing data")
        
        for i in range(30, 33):
            newMsg = HelloWorldData_Msg(userID = i , message = "Other message {0}".format(i))
            print("written sample {0} ".format(newMsg))
            rc = self.writer.write(newMsg)
        
        time.sleep(5)
        
        mask = DDS_ANY_SAMPLE_STATE | DDS_ANY_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        cnt = 0
        
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read_mask(mask)
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
            except:
                print("Error occured while trying to read data while testing read_mask")
                            
        print("Writer >> Begin writeing data")
        for i in range(33, 36):
            newMsg = HelloWorldData_Msg(userID = i , message = "Other message {0}".format(i))
            print("written sample {0} ".format(newMsg))
            rc = self.writer.write(newMsg)
        time.sleep(5)
        
        sample = HelloWorldData_Msg(userID = 33 , message = "message to dispose")
        self.writer.dispose(sample)
        time.sleep(5)
        
        mask = DDS_NOT_READ_SAMPLE_STATE | DDS_ALIVE_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read_mask(mask)
                if samples is not None:
                    print ("samples is not none")
                    samples_as_list = list(samples)    
                    for s in list(filter( lambda x: x[1].valid_data, samples_as_list)):
                        print ("scanning sample_list")
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
                            print('val_.message {}'.format( val_.message))
                                
                            self.assertTrue( val_.userID in range(30, 36) , "unexpected message read")
                            self.assertEqual(s[1].sample_state, DDS_NOT_READ_SAMPLE_STATE, "Read samples does not have the good mask")
                            self.assertEqual(s[1].instance_state, DDS_ALIVE_INSTANCE_STATE, "Read samples does not have the expected instance_state, userID = {0}".format(val_.userID))
                            
            except:
                raise Exception ("Invalid data received")
        
        self.assertEqual(cnt_samples, 2, "Wrong number of samples read")
        mask = DDS_ANY_SAMPLE_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        
        print ("Test read with mask DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE ")
        
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read_mask(mask)
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
                                
                            self.assertTrue( val_.userID is 33 , "unexpected message read")
                            self.assertEqual(s[1].instance_state, DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE, "Read samples does not have the expected instance_state")
                            
            except:
                raise Exception ("Invalid data received")
            
            
        self.assertEqual(cnt_samples, 1, "Wrong number of samples read")
    
    @unittest.skip("demonstrating skipping")
    def test_read_wl (self):
        print("Begin test_read_wl")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        
        for i in range(50, 55):
            newMsg = HelloWorldData_Msg(userID = i, message = "Other message {0}".format(i))
            print("Writer >> Begin writeing data {0}".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation did not succeed")
            time.sleep(1)
            
        time.sleep(5)
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read_wl()
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
                            
                            self.assertTrue(val_.userID in range(50, 55), "Read message has an invalid key {0}".format(val_.userID))
                            
            except:
                print ("Invalid data read")
                
        self.assertEqual(cnt_samples, 5, "read samples are not as expected")
    
    def test_read_instacne (self):
        print("Begin test_read_instance")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        
        for i in range(60, 65):
            newMsg = HelloWorldData_Msg(userID = i, message = "Other message {0}".format(i))
            print("Writer >> Begin writeing data {0}".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation did not succeed")
            time.sleep(1)
            
        time.sleep(5)
        
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read()
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
                            print("s[1].instance_handle ", s[1].instance_handle)
                            
                            self.assertTrue(val_.userID in range(60, 65), "Read message has an invalid key {0}".format(val_.userID))
                            
            except:
                print ("Invalid data read")
        
        self.assertEqual(cnt_samples, 5, "Wrong numbe of samples read")
        data = newMsg 
        
        print (">>>>>>>>>>>>>>>>>>>>>>>> data =", data)
        
        inst_hdl = self.reader.lookup_instance(data)
        
        print("inst_hdl = ", inst_hdl)
                
        self.assertIsNotNone(inst_hdl, "Instance handle is not valid a valid handle")
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read_instance loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read_instance(inst_hdl)
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
                            
                            self.assertTrue(val_.userID is  data.userID, "Read message has an invalid key {0}".format(val_.userID))
                            self.assertEqual(s[1].instance_handle, inst_hdl,"Instacne handle of read sample is not the same as the one found in lookup_instance")
                else:
                    print("No samples read")
                            
            except:
                print ("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])
        self.assertEqual(cnt_samples, 1, "read samples are not as expected")
    
    @unittest.skip("demonstrating skipping")
    def test_take (self):
        print("Begin test_read")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        
        for i in range(100, 105):
            newMsg = HelloWorldData_Msg(userID = i, message = "Other message {0}".format(i))
            print("Writer >> Begin writeing data {0}".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation did not succeed")
            time.sleep(1)
        
        time.sleep(5)
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.take()
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
                            print("s[1].instance_handle ", s[1].instance_handle)
                            
                            self.assertTrue(val_.userID in range(100, 105), "Read message has an invalid key {0}".format(val_.userID))
            except:
                print ("Invalid data read")
                raise Exception("Unexpected error:", sys.exc_info()[0])
                

        self.assertEqual(cnt_samples, 5, "read samples are not as expected")
     
    @unittest.skip("demonstrating skipping")
    def test_take_mask (self):
        print("Begin test_take_mask")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        
        print("Writer >> Begin writeing data")
        
        for i in range(110, 113):
            newMsg = HelloWorldData_Msg(userID = i , message = "Other message {0}".format(i))
            print("written sample {0} ".format(newMsg))
            rc = self.writer.write(newMsg)
        
        time.sleep(5)
        
        mask = DDS_ANY_SAMPLE_STATE | DDS_ANY_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read_mask(mask)
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
            except:
                print("Error occured while trying to read data while testing read_mask")
                            
        print("Writer >> Begin writeing data")
        for i in range(113, 116):
            newMsg = HelloWorldData_Msg(userID = i , message = "Other message {0}".format(i))
            print("written sample {0} ".format(newMsg))
            rc = self.writer.write(newMsg)
        time.sleep(5)
        
        sample = HelloWorldData_Msg(userID = 113 , message = "message to dispose")
        self.writer.dispose(sample)
        time.sleep(5)
        
        mask = DDS_READ_SAMPLE_STATE | DDS_ALIVE_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        
        cnt_samples = 0
        sample_read = False
        print('reader.take_mask >> begin read loop!')
        print ('test take_mask (\"DDS_ANY_SAMPLE_STATE | DDS_ANY_VIEW_STATE| DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE\"')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.take_mask(mask)
                if samples is not None:
                    print ("samples is not none")
                    samples_as_list = list(samples)    
                    for s in list(filter( lambda x: x[1].valid_data, samples_as_list)):
                        print ("scanning sample_list")
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
                            print('val_.message {}'.format( val_.message))
                            print ('s[1].sample_state = {0}'.format(s[1].sample_state))
                            print('s[1].instance_state {0}'.format(s[1].instance_state))
                                
                            self.assertTrue( val_.userID in range(110, 113) , "unexpected message read userID = {0}".format(val_.userID))
                            self.assertEqual(s[1].sample_state, DDS_READ_SAMPLE_STATE, "Read samples does not have the good mask")
                            self.assertEqual(s[1].instance_state, DDS_ALIVE_INSTANCE_STATE, "Read samples does not have the expected instance_state, userID = {0}".format(val_.userID))
                            
            except:
                raise Exception ("Invalid data received")
        
        self.assertEqual(cnt_samples, 3, "Wrong number of samples read")
        mask = DDS_ANY_SAMPLE_STATE | DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        
        print ("Test read with mask DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE ")
        
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.take_mask(mask)
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
                                
                            self.assertTrue( val_.userID is 113 , "unexpected message read")
                            self.assertEqual(s[1].instance_state, DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE, "Read samples does not have the expected instance_state")
                            
            except:
                raise Exception ("Invalid data received")
            
            
        self.assertEqual(cnt_samples, 1, "Wrong number of samples read")
    
    @unittest.skip("demonstrating skipping")
    def test_take_next (self):
        print("Begin test_read_mask")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        
        print("Writer >> Begin writeing data")
        
        for i in range(70, 80):
            newMsg = HelloWorldData_Msg(userID = i , message = "Other message {0}".format(i))
            print("written sample {0} ".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation failed")
            
        time.sleep(5)
        
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read_n(2)
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
                            
                            self.assertTrue(val_.userID in range(70, 80))
            except:
                print("Error occured while trying to read data while testing read_mask")
                
        self.assertEqual(cnt_samples, 2)
        
        sample = HelloWorldData_Msg(userID = 75 , message = "message to dispose")
        rc = self.writer.dispose(sample)
        self.assertEqual(rc, 0, "Dispose operation failed")
        time.sleep(5)
        
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.take_next()
                if samples is not None and len(samples) > 0:
                    self.assertEqual(len(samples), 1, "More samples read (len(samples) = {0} > 1)".format(len(samples)))
                    samples_as_list = list(samples)    
                    
                    for s in list(filter( lambda x: x[1].valid_data, samples_as_list)):
                        print ("scanning sample_list")
                        if s[0] is not None and s[1].valid_data:
                            sam = s[0]
                            cnt_samples += 1
                            
                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format( val_.message))
                                
                            self.assertTrue( val_.userID in range(70, 80) , "unexpected message read")
                            self.assertEqual(s[1].sample_state, DDS_NOT_READ_SAMPLE_STATE, "Read samples does not have the good mask")
                            if val_.userID != 75 :
                                self.assertEqual(s[1].instance_state, DDS_ALIVE_INSTANCE_STATE, "Read samples does not have the expected instance_state, userID = {0}".format(val_.userID))
                            else:
                                self.assertEqual(s[1].instance_state, DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE, "Read samples does not have the expected instance_state, userID = {0}".format(val_.userID))
                else:
                    sample_read = True
                            
            except:
                raise Exception ("Invalid data received")
        
        self.assertEqual(cnt_samples, 8, "Wrong number of samples read")
        
    @unittest.skip("demonstrating skipping")
    def test_read_next (self):
        print("Begin test_read_mask")
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        
        print("Writer >> Begin writeing data")
        
        for i in range(80, 90):
            newMsg = HelloWorldData_Msg(userID = i , message = "Other message {0}".format(i))
            print("written sample {0} ".format(newMsg))
            rc = self.writer.write(newMsg)
            self.assertEqual(rc, 0, "Write operation failed")
            
        time.sleep(5)
        
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read_n(2)
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
                            
                            self.assertTrue(val_.userID in range(80, 90))
            except:
                print("Error occured while trying to read data while testing read_mask")
                
        self.assertEqual(cnt_samples, 2)
        
        sample = HelloWorldData_Msg(userID = 85 , message = "message to dispose")
        rc = self.writer.dispose(sample)
        self.assertEqual(rc, 0, "Dispose operation failed")
        time.sleep(5)
        
        cnt_samples = 0
        sample_read = False
        print('reader>> begin read loop!')
        while(not sample_read) : 
            time.sleep(1)
            try:
                samples = self.reader.read_next()
                if samples is not None and len(samples) > 0:
                    self.assertEqual(len(samples), 1, "More samples read (len(samples) = {0} > 1)".format(len(samples)))
                    samples_as_list = list(samples)    
                    
                    for s in list(filter( lambda x: x[1].valid_data, samples_as_list)):
                        print ("scanning sample_list")
                        if s[0] is not None and s[1].valid_data:
                            sam = s[0]
                            cnt_samples += 1
                            
                            val_ = (HelloWorldData_Msg)(**sam)
                            print('********************************************************')
                            print('******************Read data was**********************')
                            print('val = {}'.format(val_))
                            print('val_.userID {}'.format(val_.userID))
                            print('val_.message {}'.format( val_.message))
                                
                            self.assertTrue( val_.userID in range(80, 90) , "unexpected message read")
                            self.assertEqual(s[1].sample_state, DDS_NOT_READ_SAMPLE_STATE, "Read samples does not have the good mask")
                            if val_.userID != 85 :
                                self.assertEqual(s[1].instance_state, DDS_ALIVE_INSTANCE_STATE, "Read samples does not have the expected instance_state, userID = {0}".format(val_.userID))
                            else:
                                self.assertEqual(s[1].instance_state, DDS_NOT_ALIVE_DISPOSED_INSTANCE_STATE, "Read samples does not have the expected instance_state, userID = {0}".format(val_.userID))
                else:
                    sample_read = True
                            
            except:
                raise Exception ("Invalid data received")
        
        self.assertEqual(cnt_samples, 8, "Wrong number of samples read")
        
     
    def get_hello_world_key_value_type_support(self):
        return self.helloworld_lib.HelloWorldDataMsg_keys

    def get_hello_world_simple_value_type_support(self):
        return self.helloworld_lib.HelloWorldData_Msg_desc
        
if __name__ == "__main__":
    unittest.main() # run all tests
