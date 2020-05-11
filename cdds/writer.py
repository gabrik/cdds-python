from .runtime import Runtime
from .dds_binding import *
import jsonpickle

from cdds import *

class Writer (Entity):
    def __init__(self, pub, topic, ps = None, listener = None):
        self.rt = Runtime.get_runtime()
        self.participant = pub.participant
        self.parent = pub
        self.topic = topic
        qos = self.rt.to_rw_qos(ps)
        
        self.keygen = self.topic.gen_key
        
        self._qos = qos
        
        self.listener = listener
        
        self.handle = self.rt.ddslib.dds_create_writer(pub.handle, topic.handle, self.qos, self.listener)
        assert (self.handle > 0)
    
    @property
    def handle(self):
        return super(Writer, self).handle
    
    @handle.setter
    def handle(self, entity):
        super(Writer, self.__class__).handle.fset (self, entity)
        
    @property
    def participant (self):
        return super(Writer, self).participant
    
    @participant.setter
    def participant(self, entity):
        super(Writer, self.__class__).participant.fset (self, entity)
        
    @property
    def qos(self):
        return super(Writer, self).qos
    
    @qos.setter
    def qos(self, qos):
        super(Writer, self.__class__).qos.fset (self, qos)
        
    def write(self, s):
        gk = self.keygen(s)
        
        kh = KeyHolder(gk)
        
        key = jsonpickle.encode(kh)
        value = jsonpickle.encode(s)
        
        sample = DDSKeyValue(key.encode(), value.encode())
        rc = self.rt.ddslib.dds_write(self.handle, byref(sample))
        
        if rc != 0:
            raise(Exception("Write failed"))
        return rc

    def write_all(self, xs):
        for x in xs:
            self.write(x)

    def dispose_instance(self, s):
        self.rt.ddslib.dds_dispose(self.handle, byref(s))