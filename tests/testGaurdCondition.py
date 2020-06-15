import unittest

__author__ = 'ADlink Technology'

from cdds import *

import os, sys

from idl_parser import parser

parser_ = parser.IDLParser()

import cdds.py_dds_utils as utils

import time

class GaurdConditionTest (unittest.TestCase):
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
        
    def testInitGaurdCond(self):
        gcond =  GaurdCondition(self.dp)
        
        self.assertIsNotNone(gcond, "Gaurd condition is not initialized correctly")
        self.assertIsInstance (gcond, GaurdCondition, "Created gaurd condition is not of the good type" )
        
    def testSetGuardCond(self):
        cond =  GaurdCondition(self.dp)
        
        self.assertIsNotNone(cond, "Gaurd condition is not initialized correctly")
        self.assertIsInstance (cond, GaurdCondition, "Created gaurd condition is not of the good type" )
        
        rt = cond.set_guard_condition(True)
        self.assertTrue(rt, "set_gaurdcondition did not return the expected result")
        
        rt = cond.set_guard_condition(False)
        self.assertTrue(rt, "set_gaurdcondition did not return the expected result")
        
    def testReadGuardCond(self):
        gcond =  GaurdCondition(self.dp)
        
        self.assertIsNotNone(gcond, "Gaurd condition is not initialized correctly")
        self.assertIsInstance (gcond, GaurdCondition, "Created gaurd condition is not of the good type" )
        
        rt = gcond.set_guard_condition(True)
        self.assertTrue(rt, "set_gaurdcondition did not return the expected result")
        
        triggered = gcond.read_trigger()
        
        self.assertIsNotNone(triggered, " read guard condition did not get expected object")
        self.assertTrue(triggered, "Read gaurdCondition did not return expected value")
        
        rt = gcond.set_guard_condition(False)
        self.assertTrue(rt, "set_gaurdcondition did not return the expected result")
        
        triggered = gcond.read_trigger()
        
        self.assertIsNotNone(triggered, " read guard condition did not get expected object")
        self.assertFalse(triggered, "Read gaurdCondition did not return expected value")
        
    def testTakeGuardCond(self):
        gcond =  GaurdCondition(self.dp)
        
        self.assertIsNotNone(gcond, "Gaurd condition is not initialized correctly")
        self.assertIsInstance (gcond, GaurdCondition, "Created gaurd condition is not of the good type" )
        
        rt = gcond.set_guard_condition(True)
        self.assertTrue(rt, "set_gaurdcondition did not return the expected result")
        
        triggered = gcond.take_trigger()
        
        self.assertIsNotNone(triggered, " take guard condition did not get expected object")
        self.assertTrue(triggered, "Take gaurdCondition did not return expected value")
        
        triggered = gcond.read_trigger()
        
        self.assertIsNotNone(triggered, " read guard condition did not get expected object")
        self.assertFalse(triggered, "Read gaurdCondition did not return expected value")
        
        rt = gcond.set_guard_condition(False)
        self.assertTrue(rt, "set_gaurdcondition did not return the expected result")
        
        triggered = gcond.take_trigger()
        
        self.assertIsNotNone(triggered, " take guard condition did not get expected object")
        self.assertFalse(triggered, "take gaurdCondition did not return expected value")
        
        triggered = gcond.read_trigger()
        
        self.assertIsNotNone(triggered, " read guard condition did not get expected object")
        self.assertFalse(triggered, "Read gaurdCondition did not return expected value")