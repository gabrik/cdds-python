import unittest

from cdds import *

__author__ = 'ADlink Technology'


class PublisherTest(unittest.TestCase):
    def setUp(self):
        self.rt = Runtime.get_runtime()
        self.participant = Participant(0)
        self.publisher = Publisher(self.participant)

    def test_initialize_subscriber(self):
        dp = Participant(0)
        pub = Publisher(dp)
        self.assertIsNotNone(pub, "Publisher is not created correctly")
        self.assertIsInstance(pub, Publisher, "Create publisher didn't produce an entity of the food type")

    def test_create_writer(self):
        topic_name = "topic_name"
        type_support = self.rt.get_key_value_type_support()
        topic = Topic(self.participant, topic_name, type_support)
        datawriter_ps = [Reliable(), KeepLastHistory(10)]
        datawriter = self.publisher.create_writer(topic, datawriter_ps)

        self.assertIsNotNone(datawriter, "Create_writer failed")
        self.assertIsInstance(datawriter, Writer, "Create_datawriter created an entity of a wrong type")

    def test_suspend_resume(self):
        rc = self.publisher.suspend()
        self.assertEqual(rc, -2, "Suspend did not return the correct return code")

        rc = self.publisher.resume()
        self.assertEqual(rc, -2, "Resume did not return the correct return code")


if __name__ == "__main__":
    unittest.main()  # run all tests
