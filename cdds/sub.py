from .runtime import Runtime
from .policy import Partition
from cdds import *

from cdds.reader import *


class Subscriber(Entity):
    def __init__(self, dp, ps=None, listener=None):
        self.rt = Runtime.get_runtime()
        self.participant = dp
        self.parent = dp
        self.handle = self.rt.ddslib.dds_create_subscriber(dp.handle, ps, listener)
        # qos = self.rt.ddslib.dds_set_qos(self.handle, self.qos)
        self.qos = ps
        self._datareader_list = []

        assert (self.handle is not None and self.handle > 0)

    @staticmethod
    def partitions(ps):
        return [Partition(ps)]

    @staticmethod
    def partition(p):
        return [Partition([p])]

    @property
    def handle(self):
        return super(Subscriber, self).handle

    @handle.setter
    def handle(self, entity):
        super(Subscriber, self.__class__).handle.fset(self, entity)

    @property
    def participant(self):
        return super(Subscriber, self).participant

    @participant.setter
    def participant(self, entity):
        super(Subscriber, self.__class__).participant.fset(self, entity)

    def create_reader(self, topic, policy=None, dr_listener=None):
        data_reader = Reader(self, topic, policy, dr_listener)
        self._datareader_list.append(data_reader)
        return data_reader

    def _check_handle(self):
        if super().handle is None:
            raise Exception('Entity is already closed')
