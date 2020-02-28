from .runtime import Runtime
from .dds_binding import DDSKeyValue
from ctypes import *

from pydds import *
from pydds.entity import *

MAX_NAME_SIZE = 100

class TopicType(object):
    def gen_key(self): None


class Topic(Entity):
    def __init__(self, dp, topic_name, type_support, data_type=None, qos=None):
        self.rt = Runtime.get_runtime()
        self._name = topic_name.encode()
        self.type_support = type_support
        
        self._qos = self.rt.to_rw_qos(qos)
        self.handle = self.rt.ddslib.dds_create_topic(dp.handle, type_support, topic_name.encode(), self.qos, None)
        
        self.parent = dp
        self.participant = dp
        
        keygen = None
        
        if keygen is None:
            self.keygen = lambda x: x.gen_key()
        else:
            self.keygen = keygen
            
        self.data_type = self.type_name()
        
        assert (self.handle > 0)
        
    def gen_key(self, s):
        return self.keygen(s)
        
    def dds_get_name(self):
        res = " "* MAX_NAME_SIZE
        result = res.encode(encoding='utf_8', errors='strict')
        rc = self.rt.ddslib.dds_get_name(self.handle, result, MAX_NAME_SIZE)
         
        if(rc >= 0):
            return str(result.decode()).split('\x00', 1)[0]
        else:
            return ""
    
    @property 
    def name(self):
        return self._name.decode()

    @name.setter
    def name(self, topic_name_str):
        self._name = topic_name_str
    
    @property
    def qos(self):
        return self._qos
    
    @qos.setter
    def qos(self, other_qos):
        self._qos = other_qos
        
    def type_name(self):
        res = " "* MAX_NAME_SIZE
        result = res.encode(encoding='utf_8', errors='strict')
        rc = self.rt.ddslib.dds_get_type_name(self.handle, result, MAX_NAME_SIZE)
         
        if(rc >= 0):
            return str(result.decode()).split('\x00', 1)[0]
         
        else:
            return ""
        
    @property
    def handle(self):
        return super(Topic, self).handle
    
    @handle.setter
    def handle(self, entity):
        super(Topic, self.__class__).handle.fset (self, entity)
        
    
        
    def _check_handle(self):
        if super().handle is None:
            raise Exception('Entity is already closed')
        
        
    
class FoundTopic (Topic):
    def __init__(self, participant):
        self.rt = Runtime.get_runtime()
        
        self.participant = participant
        self.parent = participant 