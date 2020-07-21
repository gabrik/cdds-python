from .runtime import Runtime
from .dds_binding import *
import jsonpickle

from cdds import *
from __builtin__ import None

class QoS(object):
   
    def __init__(self, policies = []):
        self.policies = policies
        self.rt = Runtime.get_runtime()
        self.handle = self.rt.ddslib.dds_create_qos()
        
    @property
    def handle(self):
        return self.handle

    @handle.setter
    def handle(self, qos_handle ):
        self.handle = qos_handle
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.policies == other.policies
        return False
    
    def copy_from(self, src):
        if src is None or not isinstance(src, self.__class__) or src.handle is None:
            raise Exception("Source QoS Policy is not initialized, please initialize it and try again")
        self.policies = src.policies
    
    def copy_to(self, destination):
        if destination is None or not isinstance(destination, self.__class__) or destination.handle is None:
            raise Exception("Destination is not initialized, please initialize it and try again")
        destination.policies = self.policies
    
    def get_durability_policy (self):
        kind = 0
        durability = self.rt.ddslib.dds_qget_durability(self.handle, byref(kind))
        return DurabilityQoSPolocy(kind)
        
    def to_rw_qos(self):
        pass