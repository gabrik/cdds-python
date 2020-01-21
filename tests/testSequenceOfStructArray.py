import unittest

from struct import *

__author__ = 'ADlink Technology'

from cdds import *
import time

class Inner_Struct(Topic):
    def __init__(self, short, double):
        super(Topic, self).__init__()
        self.short1= short
        self.double1=double
        
    def gen_key(self):
        return self.short1
    
    def __str__(self):
        return 'InnerSeq({0}, {1})'.format(self.short1, self.double1)
    
    def __eq__(self, other): 
        if not isinstance(other, Inner_Struct):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        return self.short1 == other.short1 and self.double1 == other.double1
    
    
    __repr__ = __str__
    
class Inner_Struct_Array(Topic):
    def __init__(self, seq):
        super(Topic, self).__init__()
        self.SeqArray = seq
    
    def __str__(self):
        return f'Inner_Struct_Array {self.SeqArray}' 
    
    def __getitem__(self, item_number):
        return self.SeqArray[item_number]
    
    def __eq__(self, other): 
        if not isinstance(other, Inner_Struct_Array):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        cnt = 0
        for elem in self.SeqArray:
            if elem != other.SeqArray[cnt]: return False
            cnt +=1
        
        return True  
        
    
    __repr__ = __str__
        

class SequenceOfStructArray_struct(Topic):
    def __init__(self, longID, arraySequence):
        super(Topic, self).__init__()
        self.longID = longID
        self.arraySequence = Inner_Struct_Array(arraySequence)
    
    def gen_key(self):
        return self.longID

    def __str__(self):
        return 'SequenceMessage(longID: {0}, InnerArraySeq: {1})'.format(self.longID, self.arraySequence)

class BasicTestCase(unittest.TestCase):
    def test_sendReceive(self):
        rt = Runtime()
        dp = Participant(0)
        
        self.assertTrue( dp is not None ) 
        self.assertIsInstance(dp, Participant)
        
        topic = FlexyTopic(dp, 'Sequence_struct_Topic')
        publisher = Publisher(dp)
        writer = FlexyWriter(publisher, topic, [Reliable(), TransientLocal(), KeepLastHistory(10)])
        
        cnt = 0
        
        message = SequenceOfStructArray_struct(
                13,
                ([
                    [Inner_Struct(11,1.1),Inner_Struct(12,1.2)],
                    [Inner_Struct(21,2.1),Inner_Struct(22,2.2)],
                    [Inner_Struct(31,3.1),Inner_Struct(32,3.2)]
                ]))
        
        writer.write(message)
        print('Writer wrote: {0}'.format(message))
        time.sleep(1)

        topic_reader = FlexyTopic(dp, 'Sequence_struct_Topic')
        subscriber = Subscriber(dp)
        dataReader = FlexyReader(subscriber, topic_reader, None, [Reliable(), TransientLocal(), KeepLastHistory(10)])
        
        print('reader>> waiting for a message!')
        
        messageReceived = False
        
        while not messageReceived:
            time.sleep(5)
            samples = dataReader.take(all_samples())
            
            for sample in samples:
                if sample[1].valid_data:
                    print ('received message >> {0})'.format(sample[0]))
                    
                    self.assertEqual(message.longID, sample[0].longID)
                    self.assertEqual(message.arraySequence[0],sample[0].arraySequence[0])
                    messageReceived=True
#                     if messageReceived:
#                         break

if __name__ == "__main__":
    unittest.main() # run all tests