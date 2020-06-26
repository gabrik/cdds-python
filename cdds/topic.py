from .runtime import Runtime
from .dds_binding import DDSKeyValue
from ctypes import *

from cdds import *
from cdds.entity import *
from cdds.listener import *

MAX_NAME_SIZE = 100

class InconsistentTopicStatus(Structure):
    _fields_=[("total_count", c_uint32 ) ,
              ("total_count_change", c_int32 )
            ]

def do_nothing(a, *args):
    return a

class TopicType(object):
    def gen_key(self): None
    
class Topic(Entity):
    def __init__(self, dp, topic_name, type_support, data_type=None, qos=None, topic_listener = None):
        self.rt = Runtime.get_runtime()
        self._name = topic_name.encode()
        self.type_support = type_support
        
        self._qos = self.rt.to_rw_qos(qos)
        
        if topic_listener is not None:
            if getattr(topic_listener, "on_inconsistent_topic") and callable(topic_listener.on_inconsistent_topic):
                self.inconsistent_topic_handler = topic_listener.on_inconsistent_topic
                
                self.rt.ddslib.dds_lset_inconsistent_topic (self.listener_handle, self.dispatcher.dispatch_on_inconsistent_topic)
                
                self.dispatcher = Dispatcher.get_instance()
                self.listener = Listener()
                self.listener_handle = self.listener.handle
                self.dispatcher.register_on_inconsistent_topic_listener(self.handle, self.__handle_inconsistent_topic)
        
            else:
                self.inconsistent_topic_handler = do_nothing
                self.listener = None
                self.listener_handle = None #self.listener.handle
        else:
            self.inconsistent_topic_handler = do_nothing
            self.listener = None
            self.listener_handle = None #self.listener.handle
            
#         self.dispatcher = Dispatcher.get_instance()
#         self.listener = Listener()
#         self.listener_handle = self.listener.handle
        
        self.handle = self.rt.ddslib.dds_create_topic(dp.handle, type_support, topic_name.encode(), self.qos, self.listener_handle)
        if self.handle < 0:
            print ("failed to create reader {0}".format(self.handle))
             
        assert (self.handle > 0)
        
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
        
    def get_name(self):
        res = " "* MAX_NAME_SIZE
        result = res.encode(encoding='utf_8', errors='strict')
        rc = self.rt.ddslib.dds_get_name(self.handle, result, MAX_NAME_SIZE)
         
        if(rc >= 0):
            return str(result.decode()).split('\x00', 1)[0]
        else:
            return ""
        
    def on_inconsistent_topic(self, fun):
        self.inconsistent_topic_handler = fun
        print ("topic on_inconsistent_topic")
        self.dispatcher.register_on_inconsistent_topic_listener(self.handle, self.__handle_inconsistent_topic)
        
    def __handle_inconsistent_topic(self, r, s):
        self.inconsistent_topic_handler(self, s)
        
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
        
    def inconsistent_topic_status(self):
        '''
        Return the InconsistentTopicStatus of the reader

        InconsistentTopicStatus has fields:
            total_count,
            total_count_change,

        Returns type: InconsistentTopicStatus
        '''
        try:
            self._check_handle()
            inconsistent_topic_status = InconsistentTopicStatus(0, 0)
            ret = self.rt.ddslib.dds_get_inconsistent_topic_status(self.handle, byref(inconsistent_topic_status))
            if ret < 0:
                raise DDSException('Failure retrieving deadline changed status', ret)
            status = InconsistentTopicStatus(
                inconsistent_topic_status.total_count,
                inconsistent_topic_status.total_count_change)
        except:
            print("Error occurred while trying to handle data available")
            raise Exception("Unexpected error:", sys.exc_info()[0])
        return status
        
class FoundTopic (Topic):
    def __init__(self, participant):
        self.rt = Runtime.get_runtime()
        
        self.participant = participant
        self.parent = participant 