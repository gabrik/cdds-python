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


def publsiher():
    dp = Participant(0)

    topic = FlexyTopic(dp, 'HelloWorldData_Msg')
    publisher = dp.create_publisher()

    writer = FlexyWriter(publisher, topic, [Reliable(), TransientLocal(), KeepLastHistory(10)])

    cnt = 0

    while True:
        message = HelloWorldMessage(((cnt % 2) + 1), 'Hello World {0}'.format(cnt))
        cnt += 1
        writer.write(message)
        print('Writer wrote: {0}'.format(message))
        time.sleep(1)


if __name__ == '__main__':
    publsiher()
