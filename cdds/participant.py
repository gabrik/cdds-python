from .runtime import Runtime
from cdds import pub, topic, entity
from cdds.topic import *
from cdds.entity import *
from cdds.sub import *

# DomainParticipant Wrapper


class Participant(Entity):
    def __init__(self, did):
        self.rt = Runtime.get_runtime()
        self.did = did
        self.handle = self.rt.ddslib.dds_create_participant(did, None, None)

        assert self.handle > 0, "Failed to create Domain participant"

        self._participant = self
        self._parent = self

        self._topic_list = []
        self._publisher_list = []
        self._subscriber_list = []
        self._writer_list = []
        self._reader_list = []
        self._topic_list = []

    def create_publisher(self, publisher_qos=None, publisher_listener=None):
        publisher = pub.Publisher(self, publisher_qos, publisher_listener)
        self._publisher_list.append(publisher)

        return publisher

    def create_subscriber(self, subsriber_qos=None, subscriber_listener=None):
        subscriber = Subscriber(self, subsriber_qos, subscriber_listener)
        self._subscriber_list.append(subscriber)
        return subscriber

    def create_topic(self, topic_name, type_support=None, qos=None, topic_listener=None):
        if(type_support is None):
            type_support = self.rt.get_key_value_type_support()
        t = Topic(self, topic_name, type_support, qos, topic_listener)
        self._topic_list.append(topic)
        return t

    def find_topic(self, topic_name):
        topic_name_as_byte_array = topic_name.encode(encoding='utf_8', errors='strict')
        foundTopic = self.rt.ddslib.dds_find_topic(self.handle, topic_name_as_byte_array)

        return foundTopic

    @property
    def handle(self):
        return super(Participant, self).handle

    @handle.setter
    def handle(self, e):
        super(Participant, self.__class__).handle.fset(self, e)

    def _check_handle(self):
        if super().handle is None:
            raise Exception('Entity is already closed')
        return True
