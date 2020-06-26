from .dds_binding import *
from .runtime import Runtime

from cdds import *
from cdds.dispatcher import *
from ctypes import *
    
class Dispatcher(object):
    __instance = None
    def __init__(self):
        
        if Dispatcher.__instance is None:
            self.dataListenerMap = {}
            self.subscriptionMatchedListenerMap = {}
            self.livelinessChangeListenerMap = {}
            self.requesedDeadlineMissedListenerMap = {}
            self.requestedIncompatibleQosListenerMap = {}
            self.sampleRejectedListenerMap = {}
            self.sampleLostListenerMap = {}
            
            self.inconsistent_topicMap = {}
            
            self.dataOnReaderListenerMap = {}
            
            self.publicationMatchedListenerMap = {}
            self.livelinessLostListenerMap = {}
            self.offeredDeadlineMissedListenerMap = {}
            self.offeredIncompatibleQosListenerMap = {}
            
            Dispatcher.__instance = self
        else:
            raise Exception("You can't create multiple instances of Dispatcher! you can use get_instance instead")
    
    def register_data_listener(self, handle, fun):
        h = repr(handle)
        self.dataListenerMap[h] = fun
        
    def register_on_inconsistent_topic_listener(self, handle, fun):
        h = repr(handle)
        self.inconsistent_topicMap[h] = fun

    def register_liveliness_changed_listener(self, handle, fun):
        h = repr(handle)
        self.livelinessChangeListenerMap[h] = fun

    def register_subscription_matched_listener(self, handle, fun):
        h = repr(handle)
        self.subscriptionMatchedListenerMap[h] = fun
        
        
    def register_requested_deadline_missed_listener(self, handle, fun):
        h = repr(handle)
        self.requesedDeadlineMissedListenerMap[h] = fun
        
    def register_incompatable_qos_listener(self, handle, fun):
        h = repr(handle)
        self.requestedIncompatibleQosListenerMap[h] = fun
        
    def register_on_sample_rejected_listener(self, handle, fun):
        h = repr(handle)
        self.sampleRejectedListenerMap[h] = fun
        
    def register_on_sample_lost_listener(self, handle, fun):
        h = repr(handle)
        self.sampleLostListenerMap[h] = fun
        
    def register_data_on_readers_listener(self, handle, fun):
        h = repr(handle)
        self.dataOnReaderListenerMap[h] = fun
        
    def register_liveliness_lost_listener(self, handle, fun):
        h = repr(handle)
        self.livelinessLostListenerMap[h] = fun
        
    def register_publication_matched_listener(self, handle, fun):
        
        h = repr(handle)
        self.publicationMatchedListenerMap[h] = fun
        
    def register_offered_deadline_missed_listener(self, handle, fun):
        h = repr(handle)
        self.offeredDeadlineMissedListenerMap[h] = fun
         
    def register_offered_incompatable_qos_listener(self, handle, fun):
        h = repr(handle)
        self.offeredIncompatibleQosListenerMap[h] = fun
        
    @staticmethod
    def get_instance():
        if Dispatcher.__instance is None:
            Dispatcher()
            
        return Dispatcher.__instance
    
    @staticmethod
    def dispatch_data_listener(handle, s):
        h = repr(handle)
        dispatcher_instance = Dispatcher.get_instance()
        if h in dispatcher_instance.dataListenerMap:
            fun = dispatcher_instance.dataListenerMap[h]
            fun(handle)
            
            
            
    @staticmethod
    def dispatch_subscription_matched_listener(handle, s):
        h = repr(handle)
        dispatcher_instance = Dispatcher.get_instance()
        if h in dispatcher_instance.subscriptionMatchedListenerMap:
            fun = dispatcher_instance.subscriptionMatchedListenerMap[h]
            fun(handle, s)
            
            
    @staticmethod
    def dispatch_requested_deadline_listener(handle, s):
        h = repr(handle)
        
        dispatcher_instance = Dispatcher.get_instance()
        
        if h in dispatcher_instance.requesedDeadlineMissedListenerMap:
            fun = dispatcher_instance.requesedDeadlineMissedListenerMap[h]
            fun(handle, s)
    
    @staticmethod
    def dispatch_on_offered_deadline_missed_listener(handle, s):
        h = repr(handle)
         
        dispatcher_instance = Dispatcher.get_instance()
        if h in dispatcher_instance.offeredDeadlineMissedListenerMap:
            fun = dispatcher_instance.offeredDeadlineMissedListenerMap[h]
            fun(handle, s)
    
    @staticmethod
    def dispatch_incompatable_qos_listener(handle, s):
        h = repr(handle)
        
        dispatcher_instance = Dispatcher.get_instance()
        
        if h in dispatcher_instance.requestedIncompatibleQosListenerMap:
            fun = dispatcher_instance.requestedIncompatibleQosListenerMap[h]
            fun(handle, s)


    @staticmethod
    def dispatch_offered_incompatable_qos_listener(handle, s):
        h = repr(handle)
         
        dispatcher_instance = Dispatcher.get_instance()
         
        if h in dispatcher_instance.offeredIncompatibleQosListenerMap:
            fun = dispatcher_instance.offeredIncompatibleQosListenerMap[h]
            fun(handle, s)
    
    @staticmethod
    def dispatch_liveliness_changed_listener(handle, s):
        h = repr(handle)
        dispatcher_instance = Dispatcher.get_instance()
        if h in dispatcher_instance.livelinessChangeListenerMap:
            fun = dispatcher_instance.livelinessChangeListenerMap[h]
            fun(handle, s)
            
            
    @staticmethod
    def dispatch_sample_rejected_listener(handle, s):
        h = repr(handle)
        dispatcher_instance = Dispatcher.get_instance()
        if h in dispatcher_instance.sampleRejectedListenerMap:
            fun = dispatcher_instance.sampleRejectedListenerMap[h]
            fun(handle, s)
    
    @staticmethod
    def dispatch_inconsistent_topic_listener(handle, s):
        h = repr(handle)
        dispatcher_instance = Dispatcher.get_instance()
        if h in dispatcher_instance.inconsistent_topicMap:
            fun = dispatcher_instance.inconsistent_topicMap[h]
            fun(handle, s)
    
    @staticmethod
    def dispatch_sample_lost_listener(handle, s):
        h = repr(handle)
        dispatcher_instance = Dispatcher.get_instance()
        if h in dispatcher_instance.sampleLostListenerMap:
            fun = dispatcher_instance.sampleLostListenerMap[h]
            fun(handle, s)
            
    @staticmethod
    def dispatch_data_on_reader_listener(handle):
        h = repr(handle)
        dispatcher_instance = Dispatcher.get_instance()
        if h in dispatcher_instance.dataOnReaderListenerMap:
            fun = dispatcher_instance.dataOnReaderListenerMap[h]
            fun(handle, s)
            
            
            
    @staticmethod
    def dispatch_on_publication_matched_listener(handle, s):
        h = repr(handle)
        
        dispatcher_instance = Dispatcher.get_instance()
        
        if h in dispatcher_instance.publicationMatchedListenerMap:
            fun = dispatcher_instance.publicationMatchedListenerMap[h]
            fun(handle, s)
    
    
    @staticmethod
    def dispatch_liveliness_lost_listener(handle, s):
        h = repr(handle)
        dispatcher_instance = Dispatcher.get_instance()
        if h in dispatcher_instance.livelinesslostListenerMap:
            fun = dispatcher_instance.livelinesslostListenerMap[h]
            fun(handle, s)
    
    @staticmethod
    def dispatch_offered_incompatable_qos(handle, s):
        h = repr(handle)
         
        dispatcher_instance = Dispatcher.get_instance()
         
        if h in dispatcher_instance.offeredIncompatibleQosListenerMap:
            fun = dispatcher_instance.offeredIncompatibleQosListenerMap[h]
            fun(handle, s)
    
    @LIVELINESS_CHANGED_PROTO
    def dispatch_on_liveliness_changed(r, s, a):
        # print("[python-cdds]:>>  Dispatching Liveliness change")
        Dispatcher.dispatch_liveliness_changed_listener(r, s)
        
    @LIVELINESS_LOST_PROTO
    def dispatch_on_liveliness_lost(r, s, a):
        # print("[python-cdds]:>>  Dispatching Liveliness change")
        Dispatcher.dispatch_liveliness_lost_listener(r, s)
    
    @DATA_AVAILABLE_PROTO
    def dispatch_on_data_available(r, s, a):
        # print("[python-cdds]:>>  Dispatching Data Available ")
        Dispatcher.dispatch_data_listener(r, s)
    
    
    @SUBSCRIPTION_MATCHED_PROTO
    def dispatch_on_subscription_matched(e, s, a):
        # print("[python-cdds]:>>  Dispatching Subscription Match")
        Dispatcher.dispatch_subscription_matched_listener(e, s)
        
    @PUBLICATION_MATCHED_PROTO
    def dispatch_on_publication_matched(e, s, a):
        # print("[python-cdds]:>>  Dispatching Subscription Match")
        Dispatcher.dispatch_on_publication_matched_listener(e, s)
    
    
    @REQUESTED_DEADLINE_MISSED_PROTO
    def dispatch_on_requested_deadline_missed(e, s, a):
        Dispatcher.dispatch_requested_deadline_listener(e, s)
        
    @OFFERED_DEADLINE_MISSED_PROTO
    def dispatch_on_offered_deadline_missed(e, s, a):
        Dispatcher.dispatch_on_offered_deadline_missed_listener(e, s)
    
    
    @REQUESTED_INCOMPATIBLE_QOS_PROTO
    def dispatch_on_requested_incompatable_qos (e, s, a):
        Dispatcher.dispatch_incompatable_qos_listener(e,s)
        
    @OFFERED_INCOMPATIBLE_QOS_PROTO
    def dispatch_on_offered_incompatable_qos (e, s, a):
        Dispatcher.dispatch_offered_incompatable_qos(e,s)
    
    
    @SAMPLE_REJECTED_PROTO
    def dispatch_on_sample_rejected(e, s, a):
        Dispatcher.dispatch_sample_rejected_listener(e, s)
        
    @INCONSISTENT_TOPIC_PROTO
    def dispatch_on_inconsistent_topic(e, s, a):
        # print("[python-cdds]:>>  dispatching inconsistent topic ")
        Dispatcher.dispatch_inconsistent_topic_listener(e, s)
        
    
    @DATA_ON_READERS_PROTO
    def dispatch_on_data_on_readers(e, s):
        Dispatcher.dispatch_data_on_reader_listener(e)
    
    
    @SAMPLE_LOST_PROTO
    def dispatch_on_sample_lost(e, s, a):
        Dispatcher.dispatch_sample_lost_listener(e, s)
        # print("[python-cdds]:>>  Dispatching Sample Lost")
#         global logger
#         logger.debug('DefaultListener', '>> Sample Lost')