from .runtime import Runtime
from .dds_binding import *
import jsonpickle

from cdds import *

class PublicationMatchedStatus(Structure):
    _fields_=[("total_count", c_uint32 ) ,
              ("total_count_change", c_int32 ),
              ("current_count", c_uint32) ,
              ("current_count_change", c_int32) ,
              ("last_subscription_handle", c_uint64)
            ]
    
class LivelinessLostStatus(Structure):
    _fields_=[("total_count", c_uint32 ) ,
              ("total_count_change", c_int32) 
            ]
    
class OfferedIncompatibleQosStatus(Structure):
    _fields_ =[("total_count", c_uint32 ) ,
              ("total_count_change", c_int32 ),
              ("last_policy_id", c_uint32)
            ]
    
class OfferedDeadlineMissedStatus(Structure):
    _fields_=[("total_count", c_uint32 ) ,
              ("total_count_change", c_int32),
              ("last_instance_handle", c_uint64)
            ]

def do_nothing(a, *args):
    return a

class Writer (Entity):
    def __init__(self, pub, topic, ps = None, writer_listener = None):
        self.rt = Runtime.get_runtime()
        self.participant = pub.participant
        self.parent = pub
        self.topic = topic
        
        self.keygen = self.topic.gen_key
        
        qos = self.rt.to_rw_qos(ps)
        
        self._qos = qos
        
        if writer_listener is not None:
            if getattr(writer_listener, "on_publication_matched", None) and callable(writer_listener.on_publication_matched):
                self.publicatoin_listener = writer_listener.on_publication_matched
            else:
                self.publicatoin_listener = do_nothing
                
            if getattr(writer_listener, "on_liveliness_lost", None) and callable(writer_listener.on_liveliness_lost):
                self.liveliness_listener = writer_listener.on_liveliness_lost
            else:
                self.liveliness_listener = do_nothing
            
            if getattr(writer_listener, "on_offered_deadline_missed", None) and callable(writer_listener.on_offered_deadline_missed):
                self.offered_deadline_missed_listener = writer_listener.on_offered_deadline_missed
            else:
                self.offered_deadline_missed_listener = do_nothing
            
            if getattr(writer_listener, "on_offered_incompatible_qos", None) and callable(writer_listener.on_offered_incompatible_qos):
                self.incompatible_qos_listener = writer_listener.on_offered_incompatible_qos
            else:
                self.incompatible_qos_listener = do_nothing
                
        else:
            self.publicatoin_listener = do_nothing
            self.liveliness_listener = do_nothing
            self.offered_deadline_missed_listener = do_nothing
            self.incompatible_qos_listener = do_nothing
            
        self.dispatcher = Dispatcher.get_instance()
        self.listener = Listener()
        
        self.listener_handle = self.listener.handle
                                                                                      
        self.rt.ddslib.dds_lset_liveliness_lost(self.listener_handle, self.dispatcher.dispatch_on_liveliness_lost)
        self.rt.ddslib.dds_lset_publication_matched(self.listener_handle, self.dispatcher.dispatch_on_publication_matched)
        self.rt.ddslib.dds_lset_offered_deadline_missed(self.listener_handle, self.dispatcher.dispatch_on_offered_deadline_missed)
        self.rt.ddslib.dds_lset_offered_incompatible_qos(self.listener_handle, self.dispatcher.dispatch_on_offered_incompatable_qos)
            
        self.handle = self.rt.ddslib.dds_create_writer(pub.handle, topic.handle, self.qos, self.listener_handle)
        if self.handle < 0:
            print ("failed to create reader {0}".format(self.handle))
             
        assert (self.handle > 0)
        
        
        self.dispatcher.register_publication_matched_listener(self.handle, self.__handle_pub_matched)
        self.dispatcher.register_liveliness_lost_listener(self.handle, self.__handle_liveliness_lost)
        self.dispatcher.register_offered_deadline_missed_listener(self.handle, self.__handle_missed_deadline)
        self.dispatcher.register_offered_incompatable_qos_listener (self.handle, self.__handle_incompatible_qos)

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
        
    def on_publication_matched(self, fun):
        self.publicatoin_listener = fun
        self.dispatcher.register_publication_matched_listener(self.handle, self.__handle_pub_matched)
                        
    
    def on_offered_deadline_missed(self, fun):
        self.deadline_listener = fun
        self.dispatcher.register_offered_deadline_missed_listener(self.handle, self.__handle_missed_deadline)
     
    def on_incompatible_qos (self, fun):
        self.incompatible_qos_listener = fun
        self.dispatcher.register_offered_incompatible_qos_listener(self.handle, self.__handle_incompatible_qos)
         
    def on_liveliness_lost(self, fun):
        self.liveliness_listener = fun
        self.dispatcher.register_liveliness_lost_listener(self.handle, fun)
    
    def __handle_pub_matched(self, r, s):
        self.publicatoin_listener(self, s)
        
    def __handle_missed_deadline(self, r, s):
        self.offered_deadline_missed_listener(self, s)
         
     
    def __handle_liveliness_lost(self, r, s):
        self.liveliness_listener(self, s)
        
    def __handle_incompatible_qos(self, r, s):
        self.incompatible_qos_listener(self, s)
    
    def lookup_instance (self, s):
        gk = self.keygen(s)
        kh = KeyHolder(gk)
        key = jsonpickle.encode(kh)
        value = jsonpickle.encode(s)
        sample = DDSKeyValue(key.encode(), value.encode())
        result = self.rt.ddslib.dds_lookup_instance(self.handle, byref(sample))
        
        return result
        
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

    def dispose(self, s):
        gk = self.keygen(s)
        kh = KeyHolder(gk)
        key = jsonpickle.encode(kh)
        value = jsonpickle.encode(s)
        sample = DDSKeyValue(key.encode(), value.encode())
        rc = self.rt.ddslib.dds_dispose(self.handle, byref(sample))
        if rc != 0 :
            raise Exception("Dispose operation failed, return code = {0}".format(rc))

        return rc
    
    def write_dispose(self, s):
        gk = self.keygen(s)
        kh = KeyHolder(gk)
        key = jsonpickle.encode(kh)
        value = jsonpickle.encode(s)
        sample = DDSKeyValue(key.encode(), value.encode())
        rc = self.rt.ddslib.dds_writedispose(self.handle, byref(sample))
        if rc != 0 :
            raise Exception("Dispose operation failed, return code = {0}".format(rc))
        
        return rc
    
    def publication_matched_status(self):
        '''
        Return the PublicationMatchedStatus of the reader

        PublicationMatchedStatus has fields:
            total_count,
            total_count_change,
            current_count,
            current_count_change,
            last_subscription_handle

        :rtype: PublicationMatchedStatus
        '''
        self._check_handle()
        
        publicationMatched_status = PublicationMatchedStatus(0, 0, 0, 0, 0)
        
        ret = self.rt.ddslib.dds_get_publication_matched_status(self.handle, byref(publicationMatched_status))
        if ret < 0:
            raise DDSException('Failure retrieving publication_matched_status', ret)
        status = PublicationMatchedStatus(
            publicationMatched_status.total_count,
            publicationMatched_status.total_count_change,
            publicationMatched_status.current_count,
            publicationMatched_status.current_count_change,
            publicationMatched_status.last_subscription_handle)
        
        return status
    
    def liveliness_lost_status(self):
        
        self._check_handle()
        
        livelinessLost_status = LivelinessLostStatus(0, 0)
        
        ret = self.rt.ddslib.dds_get_liveliness_changed_status(self.handle, byref(livelinessLost_status))
        if ret < 0:
            raise DDSException('Failure retrieving LIVELINESS lost status', ret)
        status = LivelinessLostStatus(
            livelinessChanged_status.total_count,
            livelinessChanged_status.total_count_change)
        
    def offered_incompatible_qos_status(self):
        '''
        Return the OfferedIncompatibleQosStatus of the reader

        OfferedIncompatibleQosStatus has fields:
            total_count,
            total_count_change,
            last_policy_id

        :returns: dds.RequestedIncompatibleQosStatus
        '''
        self._check_handle()
        offered_qos_status = OfferedIncompatibleQosStatus(0,0,0) 
        ret = self.rt.ddslib.dds_get_offered_incompatible_qos_status(self.handle, byref(incompatable_qos_status))
        if ret < 0:
            raise DDSException('Failure retrieving requested_incompatible_qos_status', ret)
        status = OfferedIncompatibleQosStatus(
            offered_qos_status.total_count,
            offered_qos_status.total_count_change,
            offered_qos_status.last_policy_id)
        return status
    
    def offered_deadline_missed_status(self):
        '''
        Return the OfferedDeadlineMissedStatus of the reader

        OfferedDeadlineMissedStatus has fields:
            total_count,
            total_count_change,
            last_instance_handle

        Returns type: OfferedDeadlineMissedStatus
        '''
        try:
            self._check_handle()
            deadline_missed_status = OfferedDeadlineMissedStatus(0, 0, 0)
            ret = self.rt.ddslib.dds_get_offered_deadline_missed_status(self.handle, byref(deadline_missed_status))
            if ret < 0:
                raise DDSException('Failure retrieving deadline changed status', ret)
            status = OfferedDeadlineMissedStatus(
                deadline_missed_status.total_count,
                deadline_missed_status.total_count_change,
                deadline_missed_status.last_instance_handle)
        except:
            print("Error occurred while trying to handle data available")
            raise Exception("Unexpected error:", sys.exc_info()[0])
        return status