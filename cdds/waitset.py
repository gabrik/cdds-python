from cdds import *
from ctypes import *
from .runtime import Runtime

class WaitSet(Entity):
    def __init__(self, dp, condition = None):
        self.rt = Runtime.get_runtime()
        self.handle = self.rt.ddslib.dds_create_waitset(dp.handle)
        self.conditions = []
        if condition is not None:
            self.conditions.append(condition)
            self.attach(condition)

    def close(self):
        self.rt.ddslib.dds_waitset_detach(self.handle, self.condition)
        self.rt.ddslib.dds_delete(self.handle)

    def wait(self, timeout= dds_infinity()):
        cs = (c_void_p * 1)()
        pcs = cast(cs, c_void_p)
        s = self.rt.ddslib.dds_waitset_wait(self.handle, byref(pcs), 100, timeout)
        
        return s

    def attach(self, condition):
        rc = self.rt.ddslib.dds_waitset_attach(self.handle, condition.handle, c_void_p(None))
        if rc != 0:
            raise Exception("attach n = {0} operation failed".format(rc))
        
        self.conditions.append(condition)
        return True
    
    def detach(self, condition):
        rc = self.rt.ddslib.dds_waitset_detach(self.handle, condition.handle)
        if rc != 0:
            raise Exception("detach n = {0} operation failed".format(rc))
        
        self.conditions.remove(condition)
        return True
    
    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    def conditions(self, condition_list):
        self._conditions = condition_list