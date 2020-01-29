from .runtime import Runtime
from .dds_binding import DDSKeyValue
from ctypes import *

from pydds import *

MAX_NAME_SIZE = 100

class TopicType(object):
    def gen_key(self): None


class FlexyTopic:
    def __init__(self, dp, name, keygen=None, qos=None):
        self.rt = Runtime.get_runtime()
        if keygen is None:
            self.keygen = lambda x: x.gen_key()
        else:
            self.keygen = keygen

        self.qos = self.rt.to_rw_qos(qos)
        self.type_support = self.rt.get_key_value_type_support()
        
        self.topic = self.rt.ddslib.dds_create_topic(dp._handle, self.type_support , name.encode(), self.qos, None)
        self.handle = self.topic
        assert (self.topic > 0)
        self.data_type = DDSKeyValue
        self.dp = dp

    def gen_key(self, s):
        return self.keygen(s)
    
    def get_name(self, topic_name):
        rc = self.rt.ddslib.dds_get_name(self.handle, topic_name)
        
        return rc
