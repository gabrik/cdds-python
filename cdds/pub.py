from .runtime import Runtime
from .policy import Partition

from cdds import *

from cdds.writer import *

class Publisher(Entity):
    def __init__(self, dp, ps = None, listener = None):
        self.rt = Runtime.get_runtime()
        self.participant = dp
        qos = None
#       if ps is not None:
#           qos = self.rt.to_ps_qos(ps)
        qos = ps
        
        self.parent = dp
        self._datawriter_list = []
        self.handle = self.rt.ddslib.dds_create_publisher(self.participant.handle, qos, listener)
        assert (self.handle is not None and self.handle > 0)
        
    @staticmethod
    def partitions(ps):
        return [Partition(ps)]

    @staticmethod
    def partition(p):
        return [Partition([p])]
    
    @property
    def handle(self):
        return super(Publisher, self).handle
    
    @handle.setter
    def handle(self, entity):
        super(Publisher, self.__class__).handle.fset (self, entity)
        
    def _check_handle(self):
        if super().handle is None:
            raise Exception('Entity is already closed')
        return True
    
    @property
    def participant (self):
        return super(Publisher, self).participant
    
    @participant.setter
    def participant(self, entity):
        super(Publisher, self.__class__).participant.fset (self, entity)

    def create_writer(self, topic, policy = None, dw_listener = None):
        data_writer = Writer(self, topic, policy, dw_listener)
        self._datawriter_list.append(data_writer)
        return data_writer
    
    def suspend (self):
        rc = self.rt.ddslib.dds_suspend(self.handle)
        
        return rc
    
    def resume(self):
        rc = self.rt.ddslib.dds_resume(self.handle)
        return rc