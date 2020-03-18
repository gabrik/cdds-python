__author__ = 'ADlink Technology'

from cdds import *
import time


class HelloWorldMessage(FlexyTopic):
    def __init__(self, userID, messageText):
        super(FlexyTopic, self).__init__()
        self.userID = userID
        self.message = messageText
    
    def gen_key(self):
        return self.userID

    def __str__(self):
        return 'HelloWorldMessage(userID: {0}, message: {1})'.format(self.userID, self.message)
    
def subscriber():
    rt = Runtime()
    dp = Participant(0)
    
    topic = FlexyTopic(dp, 'HelloWorldData_Msg')
    
    subscriber = dp.create_subscriber()
    
    dataReader = FlexyReader(subscriber, topic, None, [Reliable(), TransientLocal(), KeepLastHistory(10)])
    
    print('reader>> waiting for a message!')
    
    while True:
        time.sleep(5)

        samples = dataReader.take(all_samples())
        
        for sample in samples:
            if sample[1].valid_data:
                print ('message >> {0})'.format(sample[0]))
                

if __name__ == '__main__':
    
    subscriber()
