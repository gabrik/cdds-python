import unittest

__author__ = 'ADlink Technology'

from cdds import *
import time

class SequqnceTypeTopic(Topic):
    def __init__(self, longID, longSequence):
        super(Topic, self).__init__()
        self.longID = longID
        self.longSequence = longSequence
    
    def gen_key(self):
        return self.longID

    def __str__(self):
        return 'SequenceMessage(longID: {0}, longSequence: {1})'.format(self.longID, self.longSequence)

class BasicTestCase(unittest.TestCase):
    def test_sendReceive(self):
        rt = Runtime()
        dp = Participant(0)
        
        self.assertTrue( dp is not None ) 
        self.assertIsInstance(dp, Participant)
        
        topic = FlexyTopic(dp, 'Sequence_Topic')
        publisher = Publisher(dp)
        writer = FlexyWriter(publisher, topic, [Reliable(), TransientLocal(), KeepLastHistory(10)])
        
        cnt = 0
        
        
        message = SequqnceTypeTopic( 1, [21, 32, 43])
        cnt += 1
        writer.write(message)
        print('Writer wrote: {0}'.format(message))
        time.sleep(1)

        topic_reader = FlexyTopic(dp, 'Sequence_Topic')
        
        subscriber = Subscriber(dp)
        
        dataReader = FlexyReader(subscriber, topic_reader, None, [Reliable(), TransientLocal(), KeepLastHistory(10)])
        
        print('reader>> waiting for a message!')
        
        messageReceived = False
        
        while not messageReceived:
            time.sleep(5)
            samples = dataReader.take(all_samples())
            
            for sample in samples:
                if sample[1].valid_data:
                    print ('message >> {0})'.format(sample[0]))
                    messageReceived=True
                    

if __name__ == "__main__":
    unittest.main() # run all tests