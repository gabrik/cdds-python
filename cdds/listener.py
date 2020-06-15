from .dds_binding import *
from .runtime import Runtime

from cdds import *
from ctypes import *

class SubscriptionMatchedStatus(Structure):
    _fields_=[("total_count", c_uint32 ) ,
              ("total_count_change", c_int32 ),
              ("current_count", c_uint32) ,
              ("current_count_change", c_int32) ,
              ("last_publication_handle", c_uint64)
            ]
    
class livelinessChangedStatus(Structure):
    _fields_=[("alive_count", c_uint32 ) ,
              ("not_alive_count", c_uint32 ),
              ("alive_count_change", c_int32) ,
              ("not_alive_count_change", c_int32),
              ("last_publication_handle", c_uint64)
            ]
    
class RequestedDeadlineMissedStatus(Structure):
    _fields_=[("total_count", c_uint32),
              ("total_count_change", c_int32),
              ("last_instance_handle", c_uint64)
            ]

class Listener(object):
    def __init__(self):
        self.rt = Runtime.get_runtime()
        self.__handle = self.rt.ddslib.dds_create_listener(None)
        
        self.dispatcher = Dispatcher.get_instance()
        
    
    '''
    A participant registered a topic inconsistent with a locally registered one.

    This notification applies to: Topic and Participant
    '''
    def on_inconsistent_topic(self, topic, status):
        pass
    
    '''
    A locally created data writer has failed to adhere it's DeadlinePolicy.
    This notification applies to: Writer, Publisher and Participant
    
    '''
    def on_offered_deadline_missed(self, writer, status):
        pass

    '''
    A data writer could not be matched with a data reader because of Qos incompatibilities

    This notification applies to: Writer, Publisher and Participant
    '''
    def on_offered_incompatible_qos(self, writer, status):
        pass

    '''
    A data writer has not met its committed LivelinessQosPolicy

    This notification applies to: Writer, Publisher and Participant
    '''
    def on_liveliness_lost(self, writer, status):
        pass
    
    '''
    The number of data readers matched to writer has changed.

    This notification applies to: Writer, Publisher and Participant
    '''
    def on_publication_matched(self, writer, status):
        pass
    
    
    '''
    Data is available on the passed data reader.

    This notification applies: Reader, Subscriber or Participant
    '''
    def on_data_available(self, reader):
        pass
    
    '''
    A data reader could not be matched with a data writer because of Qos incompatibilities

    This notification applies to: Reader, Subscriber and Participant
    '''
    def on_requested_incompatible_qos(self, reader, status):
        pass

    '''
    The data reader did not receive samples because of the ResourceLimitsQosPolicy

    This notification applies to: Reader, Subscriber and Participant
    '''
    def on_sample_rejected(self, reader, status):
        pass

    '''on_liveliness_changed(reader, status)
    A data reader has experienced a liveliness change in a match writer

    This notification applies to: Reader, Subscriber and Participant
    '''
    def on_liveliness_changed(self, reader, status):
        pass


    '''
    The number of data writers matched to a reader has changed.

    This notification applies to: Reader, Subscriber and Participant
    '''
    def on_subscription_matched(self, reader, status):
        pass

    '''
    A reader's requested DeadlinePolicy was not met by it's matched writers.

    This notification applies to: Reader, Subscriber and Participant
    '''
    def on_requested_deadline_missed(self, reader, status):
        pass
    
    '''
    A sample for the data reader has been lost

    This notification applies to Reader, Subscriber and Participant
    '''
    def on_sample_lost(self, reader, status):
        pass

    '''
    One or more data readers belonging to the subscriber have data available.

    This notification applies to: Subscriber and Domain Participant
    '''
    def on_data_on_readers(self, subscriber):
        pass
    
    @property
    def handle(self):
        return self.__handle
    
    @handle.setter
    def handle(self, listener_handle):
        self.__handle = listener_handle