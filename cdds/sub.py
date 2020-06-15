from .runtime import Runtime
from .policy import  Partition
from cdds import *

from cdds.reader import *

def do_nothing(a, *args):
    return a

class Subscriber(Entity):
    def __init__(self, dp, ps = None, subscriber_listener = None):
        self.rt = Runtime.get_runtime()
        self.participant = dp
        self.parent = dp
        self.qos = ps
        self._datareader_list = []
        
        if subscriber_listener is not None:
            if getattr(subscriber_listener, "on_data_on_readers") and callable(subscriber_listener.on_data_on_readers):
                print("data on readers listener set")
                self.data_on_readers_listener = subscriber_listener.on_data_on_readers
            else:
                self.data_on_readers_listener = do_nothing
        else:
            self.data_on_readers_listener = do_nothing
            
        self.dispatcher = Dispatcher.get_instance()
        self.listener = Listener()
        self.listener_handle = self.listener.handle
        
        self.handle = self.rt.ddslib.dds_create_subscriber(dp.handle, ps, self.listener_handle)
        # qos = self.rt.ddslib.dds_set_qos(self.handle, self.qos)
        self.rt.ddslib.dds_lset_data_on_readers(self.listener_handle, self.dispatcher.dispatch_on_data_on_readers)

        assert (self.handle is not None and self.handle > 0)
        self.dispatcher.register_data_on_readers_listener(self.handle, self.__handle_data_on_readers)

    
    def on_data_on_readers(self, fun):
        self.data_on_readers_listener = fun
        
    def __handle_data_on_readers(self):
        self.data_on_readers_listener (self)
    
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
        super(Subscriber, self.__class__).handle.fset (self, entity)
        
    @property
    def participant (self):
        return super(Subscriber, self).participant
    
    @participant.setter
    def participant(self, entity):
        super(Subscriber, self.__class__).participant.fset (self, entity)
        
    def create_reader(self, topic, policy = None, dr_listener = None):
        data_reader = Reader(self, topic, policy, dr_listener)
        self._datareader_list.append(data_reader)
        return data_reader
    
    def _check_handle(self):
        if super().handle is None:
            raise Exception('Entity is already closed')