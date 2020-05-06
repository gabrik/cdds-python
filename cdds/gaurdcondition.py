from .dds_binding import *
from .runtime import Runtime

from cdds import *
from ctypes import c_bool


class GaurdCondition (Entity):
    def __init__(self, entity):
        self.rt = Runtime.get_runtime()
        self.participant = entity.participant
        self.parent = entity
        
        self.handle = self.rt.ddslib.dds_create_guardcondition(entity.handle)
        
    def set_guard_condition(self, triggerd = True):
        ret = self.rt.ddslib.dds_set_guardcondition( self.handle, triggerd)
        if ret != 0 :
            print("Error while executing set_gaurdcondition")
            
        return True
        
    def read (self):
        triggered = POINTER(c_bool)()
        ret = self.rt.ddslib.dds_read_guardcondition(self.handle, byref(triggered))
        
        if ret == 0:
            return triggered
        
        return None
    
    def take (self):
        triggered = POINTER(c_bool)()
        ret = self.rt.ddslib.dds_take_guardcondition(self.handle, byref(triggered))
        
        if ret == 0:
            return triggered
        
        return None