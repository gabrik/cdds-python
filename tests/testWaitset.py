import unittest

__author__ = 'ADlink Technology'

from cdds import *

import os, sys

from idl_parser import parser

parser_ = parser.IDLParser()

import cdds.py_dds_utils as utils

import time

class WaitsetTest (unittest.TestCase):
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
        
    def tearDown(self):
        self.rt.close()
        
    def test_init_Waitset(self):
        ws0 = WaitSet(self.dp)
        self.assertIsNotNone(ws0, "Waitset Constructor created an invalid object")
        self.assertIsInstance(ws0, WaitSet, "Waitset constructor created an object of not expected type")
        
        mask = DDS_ANY_SAMPLE_STATE | DDS_ANY_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        cond = ReadCondition( self.reader, mask)
        self.assertIsNotNone(cond, "ReadCondition creation faild")
        
        ws = WaitSet(self.dp, cond)
        self.assertIsNotNone(ws, "Waitset Constructor created an invalid object")
        self.assertIsInstance(ws, WaitSet, "Waitset constructor created an object of not expected type")
        
    def test_attach(self):
        mask = DDS_ANY_SAMPLE_STATE | DDS_ANY_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        cond = ReadCondition( self.reader, mask)
        self.assertIsNotNone(cond, "ReadCondition creation failed")
        
        ws = WaitSet(self.dp)
        self.assertIsNotNone(ws, "Waitset Constructor created an invalid object")
        self.assertIsInstance(ws, WaitSet, "Waitset constructor created an object of not expected type")
        
        rc = ws.attach(cond)
        self.assertTrue(rc, "Attach did not return the expected result")
        
        cond_list = ws.conditions
        self.assertIsNotNone(cond_list, "Attached conditions of the waitset after attach operation is an invalid value")
        self.assertIn(cond, cond_list, "Condition is not attached to the condition list as expected")
        
        
    def test_detach(self):
        mask = DDS_ANY_SAMPLE_STATE | DDS_ANY_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        cond = ReadCondition( self.reader, mask)
        self.assertIsNotNone(cond, "ReadCondition creation failed")
        
        ws = WaitSet(self.dp)
        self.assertIsNotNone(ws, "Waitset Constructor created an invalid object")
        self.assertIsInstance(ws, WaitSet, "Waitset constructor created an object of not expected type")
        
        rc = ws.attach(cond)
        self.assertTrue(rc, "Attach did not return the expected result")
        
        cond_list = ws.conditions
        self.assertIsNotNone(cond_list, "Attached conditions of the waitset after attach operation is an invalid value")
        self.assertIn(cond, cond_list, "Condition is not attached to the condition list as expected")
        
        rc = ws.detach(cond)
        self.assertTrue(rc, "Attach did not return the expected result")
        
        cond_list = ws.conditions
        self.assertIsNotNone(cond_list, "Attached conditions of the waitset after attach operation is an invalid value")
        self.assertNotIn(cond, cond_list, "Condition is not attached to the condition list as expected")
        
    def test_wait(self):
        mask = DDS_ANY_SAMPLE_STATE | DDS_ANY_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        cond = ReadCondition( self.reader, mask)
        self.assertIsNotNone(cond, "ReadCondition creation failed")
        
        ws = WaitSet(self.dp)
        self.assertIsNotNone(ws, "Waitset Constructor created an invalid object")
        self.assertIsInstance(ws, WaitSet, "Waitset constructor created an object of not expected type")
        
        rc = ws.attach(cond)
        self.assertTrue(rc, "Attach did not return the expected result")
        cond_list = ws.conditions
        self.assertIsNotNone(cond_list, "Attached conditions of the waitset after attach operation is an invalid value")
        self.assertIn(cond, cond_list, "Condition is not attached to the condition list as expected")
        
        rc = ws.wait(dds_secs(1))
        
        self.assertEqual(rc, 0, "The number of triggered entity is not correct")
        
        idl_path = '/home/firas/cyclone/cdds-python/lexer/example.idl'
        className = "HelloWorldData_Msg"
        HelloWorldData_Msg = utils.create_class(className , idl_path)
        
        i = 1
        newMsg = HelloWorldData_Msg(userID = i, message = "Other message {0}".format(i))
        print("Writer >> Begin writeing data")
        rc = self.writer.write(newMsg)
            
        rc = ws.wait(dds_secs(5))
        
        self.assertEqual(rc, 1, "The number of triggered entity is not correct")
        
        mask1 = DDS_NOT_READ_SAMPLE_STATE | DDS_ANY_INSTANCE_STATE | DDS_ANY_VIEW_STATE
        cond1 = ReadCondition( self.reader, mask1)
        self.assertIsNotNone(cond1, "ReadCondition creation failed")
        
        rc = ws.attach(cond1)
        
        i = 2
        newMsg = HelloWorldData_Msg(userID = i, message = "Other message {0}".format(i))
        print("Writer >> Begin writeing data")
        rc = self.writer.write(newMsg)
        
        rc = ws.wait(dds_secs(5))
        self.assertEqual(rc, 2, "The number of triggered entity is not correct")