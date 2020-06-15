from .dds_binding import *
import jsonpickle
from .runtime import Runtime

from cdds import *
from cdds.listener import *

from collections import namedtuple

_Sample = namedtuple('_Sample',['data','status'])


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
        
        
class RequestedIncompatableQosStatus(Structure):
    _fields_=[("total_count", c_uint32),
              ("total_count_change", c_int32),
              ("last_policy_id", c_uint32)
            ]
    
class SampleRejectedStatus(Structure):
    _fields_=[("total_count", c_uint32),
              ("total_count_change", c_int32),
              ("last_reason", c_uint32),
              ("last_instance_handle", c_uint64)
            ]
    
class SampleLostStatus(Structure):
    _fields_=[("total_count", c_uint32),
              ("total_count_change", c_int32)
            ]

def do_nothing(a, *args):
    return a


def read_samples():
    return c_uint(DDS_READ_SAMPLE_STATE | DDS_ALIVE_INSTANCE_STATE | DDS_ANY_VIEW_STATE)


def new_samples():
    return c_uint(DDS_NOT_READ_SAMPLE_STATE | DDS_ALIVE_INSTANCE_STATE | DDS_ANY_VIEW_STATE)


def all_samples():
    return c_uint(DDS_ANY_STATE)


def new_instance_samples():
    return c_uint(DDS_NOT_READ_SAMPLE_STATE | DDS_ALIVE_INSTANCE_STATE | DDS_NEW_VIEW_STATE)


def not_alive_instance_samples():
    return c_uint(DDS_ANY_SAMPLE_STATE | DDS_ANY_VIEW_STATE | DDS_NOT_ALIVE_NO_WRITERS_INSTANCE_STATE)

class Reader (Entity):
    def __init__(self, sub, topic, ps=None, readerListener=None):
        self.rt = Runtime.get_runtime()
        self.participant = sub.participant
        self.parent = sub
        self.topic = topic
        
        self.keygen = self.topic.gen_key
        
        qos = self.rt.to_rw_qos(ps)
        
        self._qos = qos
        
        if readerListener is not None:
            if getattr(readerListener, "on_data_available", None) and callable(readerListener.on_data_available):
                self.data_listener = readerListener.on_data_available
            else:
                self.data_listener = do_nothing
                
            if getattr(readerListener, "on_requested_incompatible_qos", None) and callable(readerListener.on_requested_incompatible_qos):
                self.incompatible_qos_listener = readerListener.on_requested_incompatible_qos
            else:
                self.incompatible_qos_listener = do_nothing
            
            if getattr(readerListener, "on_subscription_matched", None) and callable(readerListener.on_subscription_matched):
                self.subsciption_listener = readerListener.on_subscription_matched
            else:
                self.subsciption_listener = do_nothing
                
            if getattr(readerListener, "on_liveliness_changed", None) and callable(readerListener.on_liveliness_changed):
                self.liveliness_listener = readerListener.on_liveliness_changed
            else:
                self.liveliness_listener = do_nothing
                
            if getattr(readerListener, "on_requested_deadline_missed", None) and callable(readerListener.on_requested_deadline_missed):
                self.requested_deadline_missed_listener = readerListener.on_requested_deadline_missed
            else:
                self.requested_deadline_missed_listener = do_nothing
            
            if getattr(readerListener, "on_sample_rejected", None) and callable(readerListener.on_sample_rejected):
                self.sample_rejected_listener = readerListener.on_sample_rejected
            else:
                self.sample_rejected_listener = do_nothing
            
            if getattr(readerListener, "on_sample_lost", None) and callable(readerListener.on_sample_lost):
                self.sample_lost_listener = readerListener.on_sample_lost
            else:
                self.sample_lost_listener = do_nothing
            
        else:
            self.data_listener = do_nothing
            self.subsciption_listener = do_nothing
            self.liveliness_listener = do_nothing
            self.requested_deadline_missed_listener = do_nothing
            self.incompatible_qos = do_nothing
            self.sample_rejected_listener = do_nothing
            self.sample_lost_listener = do_nothing
        
        self.dispatcher = Dispatcher.get_instance()
        self.listener = Listener()
        self.listener_handle = self.listener.handle
        self.rt.ddslib.dds_lset_data_available(self.listener_handle , self.dispatcher.dispatch_on_data_available)
        self.rt.ddslib.dds_lset_liveliness_changed(self.listener_handle, self.dispatcher.dispatch_on_liveliness_changed)
        self.rt.ddslib.dds_lset_subscription_matched(self.listener_handle, self.dispatcher.dispatch_on_subscription_matched)
        self.rt.ddslib.dds_lset_requested_deadline_missed(self.listener_handle, self.dispatcher.dispatch_on_requested_deadline_missed)
        self.rt.ddslib.dds_lset_requested_incompatible_qos(self.listener_handle, self.dispatcher.dispatch_on_requested_incompatable_qos)
        self.rt.ddslib.dds_lset_sample_rejected(self.listener_handle, self.dispatcher.dispatch_on_sample_rejected)
        self.rt.ddslib.dds_lset_sample_lost(self.listener_handle, self.dispatcher.dispatch_on_sample_lost)
            
            
        self.handle = self.rt.ddslib.dds_create_reader(sub.handle, self.topic.handle, self.qos, self.listener_handle)
        
        if self.handle <= 0:
            print ("failed to create reader {0}".format(self.handle))
        
        assert (self.handle > 0)
        self.dispatcher.register_data_listener(self.handle, self.__handle_data)
        self.dispatcher.register_subscription_matched_listener(self.handle, self.__handle_sub_matched)
        self.dispatcher.register_liveliness_changed_listener(self.handle, self.__handle_liveliness_change)
        self.dispatcher.register_requested_deadline_missed_listener(self.handle, self.__handle_missed_deadline)
        self.dispatcher.register_incompatable_qos_listener (self.handle, self.__handle_incompatible_qos)
        self.dispatcher.register_on_sample_rejected_listener (self.handle, self.__handle_sample_rejected)
        self.dispatcher.register_on_sample_lost_listener (self.handle, self.__handle_sample_lost)

    @property
    def handle(self):
        return super(Reader, self).handle
    
    @handle.setter
    def handle(self, entity):
        super(Reader, self.__class__).handle.fset (self, entity)
        
    @property
    def participant (self):
        return super(Reader, self).participant
    
    @participant.setter
    def participant(self, entity):
        super(Reader, self.__class__).participant.fset (self, entity)
        
    @property
    def qos(self):
        return super(Reader, self).qos
    
    @qos.setter
    def qos(self, qos):
        super(Reader, self.__class__).qos.fset (self, qos)

    def on_data_available(self, fun):
        self.data_listener = fun

    def on_subscription_matched(self, fun):
        self.subsciption_listener = fun
        self.dispatcher.register_subscription_matched_listener(self.handle, self.__handle_sub_matched)

    def on_liveliness_changed(self, fun):
        self.liveliness_listener = fun
        self.dispatcher.register_liveliness_changed_listener(self.handle, self.__handle_liveliness_change)
        
    def on_requested_deadline_missed(self, fun):
        self.deadline_listener = fun
        self.dispatcher.register_requested_deadline_missed_listener(self.handle, self.__handle_missed_deadline)
        
    def on_incompatible_qos(self, fun):
        self.deadline_listener = fun
        self.dispatcher.register_requested_incompatible_qos_listener(self.handle, self.__handle_incompatible_qos)
        
    def on_sample_rejected(self, fun):
        self.on_sample_rejected = fun
        self.dispatcher.register_on_sample_rejected_listener(self.handle, self.__handle_sample_rejected)
        
    def on_sample_lost(self, fun):
        self.on_sample_lost = fun
        self.dispatcher.register_on_sample_lost_listener(self.handle, self.__handle_sample_lost)

    def __handle_data(self, r):
        self.data_listener(self)

    def __handle_sub_matched(self, r, s):
        self.subsciption_listener(self, s)

    def __handle_liveliness_change(self, r, s):
        self.liveliness_listener(self, s)
        
    def __handle_missed_deadline(self, r, s):
        self.requested_deadline_missed_listener(self, s)
        
    def __handle_incompatible_qos (self, r, s):
        self.incompatible_qos_listener(self, s)
        
    def __handle_sample_rejected(self, r, s):
        self.sample_rejected_listener(self, s)
        
    def __handle_sample_lost(self, r, s):
        self.sample_lost_listener(self, s)

    def wait_for_data(self, selector, timeout):
        condition = c_void_p(self.rt.ddslib.dds_create_readcondition(self.handle, selector))
        ws = WaitSet(self.dp, condition)
        r = ws.wait(timeout)
        ws.close()
        return r

    # sread is the synchronous read, that means this blocks until some data is received
    def sread(self, selector, timeout):
        if self.wait_for_data(selector, timeout):
            return self.read(selector)
        else:
            return []

    def read(self):
        ivec = (SampleInfo * MAX_SAMPLES)()
        infos = cast(ivec, POINTER(SampleInfo))
        
        samples = (c_void_p * MAX_SAMPLES)()
        nr = self.rt.ddslib.dds_read (self.handle, samples, infos, MAX_SAMPLES, MAX_SAMPLES)
        if nr < 0 :
            raise Exception("Read n = {0} operation failed".format(nr))
        data = []
        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
            if infos[i].valid_data:
                
                si =  infos[i]
                data.append( _Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8') ),  si) )
                
        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0:
            raise Exception("Read_instance exception whlie return loan rc = {0} operation failed".format(nr))
        return data
    
    def read_mask (self, mask):
        ivec = (SampleInfo * MAX_SAMPLES)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * MAX_SAMPLES)()
        
        nr = self.rt.ddslib.dds_read_mask(self.handle, samples, infos, MAX_SAMPLES, MAX_SAMPLES, mask)
        if nr < 0 :
            raise Exception("Read n = {0} operation failed".format(nr))
        
        data = []
        
        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
            if infos[i].valid_data:
                si =  infos[i]
                data.append( _Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8') ),  si) )
                
        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0:
            raise Exception("Read_instance exception whlie return loan rc = {0} operation failed".format(nr))
        
        return data

    def read_n(self, n):
        ivec = (SampleInfo * n)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * n)()

        nr = self.rt.ddslib.dds_read (self.handle, samples, infos, n, n)
        
        if nr < 0 :
            raise Exception("Read n = {0} operation failed".format(nr))
        
        data = []
        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
            
            if infos[i].valid_data:
                si =  infos[i]
                data.append( _Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8') ),  si) )
        return data

    def read_wl (self):
        ivec = (SampleInfo * MAX_SAMPLES)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * MAX_SAMPLES)()
        nr = self.rt.ddslib.dds_read_wl (self.handle, samples, infos, MAX_SAMPLES, MAX_SAMPLES)
        
        if nr < 0 :
            raise Exception("Read operation with loan failed, return code is {0}".format(nr))
        
        data = []
        
        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
            if infos[i].valid_data:
                si =  infos[i]
                data.append( _Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8') ),  si) )
        
        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
                
        if rc != 0 :
            raise Exception("Error while return loan, retuen code = {}".format(rc))
        return data

    def lookup_instance (self, s):
        gk = self.keygen(s)
        
        kh = KeyHolder(gk)
        
        key = jsonpickle.encode(kh)
        value = jsonpickle.encode(s)
        
        sample = DDSKeyValue(key.encode(), value.encode())
        result = self.rt.ddslib.dds_lookup_instance(self.handle, byref(sample))
        
        return result

    def read_instance (self, instacne_handle):
        ivec = (SampleInfo * MAX_SAMPLES)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * MAX_SAMPLES)()
        
        nr = self.rt.ddslib.dds_read_instance (self.handle, samples, infos, MAX_SAMPLES, MAX_SAMPLES, c_uint64(instacne_handle))
        
        if nr < 0 :
            raise Exception("Read n = {0} operation failed".format(nr))
        
        data = []
        
        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
            if infos[i].valid_data:
                
                si =  infos[i]
                data.append( _Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8') ),  si) )
                
        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0:
            raise Exception("Read_instance exception whlie return loan rc = {0} operation failed".format(nr))
        
        return data

    def sread_n(self, n, selector, timeout):
        if self.wait_for_data(selector, timeout):
            return self.read_n(n, selector)
        else:
            return []

    def take(self):
        ivec = (SampleInfo * MAX_SAMPLES)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * MAX_SAMPLES)()
        
        data = []
        try:
          
            nr = self.rt.ddslib.dds_take(self.handle, samples, infos, MAX_SAMPLES, MAX_SAMPLES)
            if nr < 0:
                raise ("Error while trying to take samples, return code = {0}".format(nr))
            
            for i in range(nr):
                sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
                if infos[i].valid_data:
                    si =  infos[i]
                    data.append( _Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8') ),  si) )
        except:
            raise Exception("Error in take operation, return code = {0}".format(nr))
        return data

    def take_mask(self, mask):
        ivec = (SampleInfo * MAX_SAMPLES)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * MAX_SAMPLES)()
        
        data = []
        try:
          
            nr = self.rt.ddslib.dds_take_mask(self.handle, samples, infos, MAX_SAMPLES, MAX_SAMPLES, mask)
            if nr < 0:
                raise ("Error while trying to take samples with mask, return code = {0}".format(nr))
            
            for i in range(nr):
                sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
                if infos[i].valid_data:
                    si =  infos[i]
                    data.append( _Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8') ),  si) )
        except:
            raise Exception("Error in take_mask operation, return code = {0}".format(nr))
        return data

    def take_next(self):
        ivec = (SampleInfo * MAX_SAMPLES)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * MAX_SAMPLES)()
        
        data = []
        try:
          
            nr = self.rt.ddslib.dds_take_next(self.handle, samples, infos)
            if nr < 0:
                raise ("Error while trying to take samples, return code = {0}".format(nr))
            
            for i in range(nr):
                sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
                if infos[i].valid_data:
                    si =  infos[i]
                    data.append( _Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8') ),  si) )
        except:
            raise Exception("Error in take operation, return code = {0}".format(nr))
        return data

    def read_next(self):
        ivec = (SampleInfo * MAX_SAMPLES)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * MAX_SAMPLES)()
        
        data = []
        try:
          
            nr = self.rt.ddslib.dds_read_next(self.handle, samples, infos)
            if nr < 0:
                raise ("Error while trying to take samples, return code = {0}".format(nr))
            
            for i in range(nr):
                sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
                if infos[i].valid_data:
                    si =  infos[i]
                    data.append( _Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8') ),  si) )
        except:
            raise Exception("Error in take operation, return code = {0}".format(nr))
        return data

    def stake(self, selector, timeout):
        if self.wait_for_data(selector, timeout):
            return self.take(selector)
        else:
            return []

    def stake_n(self, n, selector, timeout):
        if self.wait_for_data(selector, timeout):
            return self.take_n(n, selector)
        else:
            return []
    
    def take_n(self, n, sample_selector):
        ivec = (SampleInfo * n)()
        infos = cast(ivec, POINTER(SampleInfo))

        SampleVec_t = c_void_p * n
        samples = SampleVec_t()
        nr = self.rt.ddslib.dds_take_mask_wl(self.handle, samples, infos, n, sample_selector)
        data = []

        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(self.topic.data_type))
            if infos[i].valid_data:
                si =  infos[i]
                data.append( _Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8') ),  si) )

        self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        return data

    def wait_history(self, timeout):
        return self.rt.ddslib.dds_reader_wait_for_historical_data(self.handle, timeout)
    
    def subscription_matched_status(self):
        '''
        Return the SubscriptionMatchedStatus of the reader

        SubscriptionMatchedStatus has fields:
            total_count,
            total_count_change,
            current_count,
            current_count_change,
            last_publication_handle

        :rtype: SubscriptionMatchedStatus
        '''
        self._check_handle()
        
        subscriptionMatched_status = SubscriptionMatchedStatus(0, 0, 0, 0, 0)
        
        ret = self.rt.ddslib.dds_get_subscription_matched_status(self.handle, byref(subscriptionMatched_status))
        if ret < 0:
            raise DDSException('Failure retrieving subscription_matched_status', ret)
        status = SubscriptionMatchedStatus(
            subscriptionMatched_status.total_count,
            subscriptionMatched_status.total_count_change,
            subscriptionMatched_status.current_count,
            subscriptionMatched_status.current_count_change,
            subscriptionMatched_status.last_publication_handle)
        
        return status
    
    def liveliness_changed_status(self):
        
        self._check_handle()
        
        livelinessChanged_status = livelinessChangedStatus(0, 0, 0, 0, 0)
        
        ret = self.rt.ddslib.dds_get_liveliness_changed_status(self.handle, byref(livelinessChanged_status))
        if ret < 0:
            raise DDSException('Failure retrieving lIVELINESS changed status', ret)
        status = livelinessChangedStatus(
            livelinessChanged_status.alive_count,
            livelinessChanged_status.not_alive_count,
            livelinessChanged_status.alive_count_change,
            livelinessChanged_status.not_alive_count_change,
            livelinessChanged_status.last_publication_handle)
        
        return status
    
    def requested_deadline_missed_status(self):
        '''
        Return the RequestedDeadlineMissedStatus of the reader

        RequestedDeadlineMissedStatus has fields:
            total_count,
            total_count_change,
            last_instance_handle

        Returns type: RequestedDeadlineMissedStatus
        '''
        try:
            self._check_handle()
            deadline_missed_status = RequestedDeadlineMissedStatus(0, 0, 0)
            ret = self.rt.ddslib.dds_get_requested_deadline_missed_status(self.handle, byref(deadline_missed_status))
            if ret < 0:
                raise DDSException('Failure retrieving lIVELINESS changed status', ret)
            status = RequestedDeadlineMissedStatus(
                deadline_missed_status.total_count,
                deadline_missed_status.total_count_change,
                deadline_missed_status.last_instance_handle)
        except:
            print("Error occurred while trying to handle data available")
            raise Exception("Unexpected error:", sys.exc_info()[0])
        return status
    
    def requested_incompatible_qos_status(self):
        '''
        Return the RequestedIncompatibleQosStatus of the reader

        RequestedIncompatibleQosStatus has fields:
            total_count,
            total_count_change,
            last_policy_id

        :returns: dds.RequestedIncompatibleQosStatus
        '''
        self._check_handle()
        incompatable_qos_status = RequestedIncompatableQosStatus(0,0,0) 
        ret = self.rt.ddslib.dds_get_requested_incompatible_qos_status(self.handle, byref(incompatable_qos_status))
        if ret < 0:
            raise DDSException('Failure retrieving requested_incompatible_qos_status', ret)
        status = RequestedIncompatableQosStatus(
            incompatable_qos_status.total_count,
            incompatable_qos_status.total_count_change,
            incompatable_qos_status.last_policy_id)
        return status
    
    
    def get_rejected_sample_status(self):
        '''
        Return the SampleRejectedStatus of the reader

        SampleRejectedStatus has fields:
            total_count,
            total_count_change,
            last_reason,
            last_instance_handle

        :rtype: SampleRejectedStatus
        '''
        self._check_handle()
        sample_rejected_status = SampleRejectedStatus (0, 0, 0, 0)
        
        ret = self.rt.ddslib.dds_get_sample_rejected_status (self.handle, byref(sample_rejected_status))
        if ret < 0:
            raise DDSException('Failure retrieving sample_rejected_status', ret)
        status = SampleRejectedStatus(
            sample_rejected_status.total_count,
            sample_rejected_status.total_count_change,
            sample_rejected_status.last_reason,
            sample_rejected_status.last_instance_handle)
        return status
    
    
    def get_lost_sample_status(self):
        '''
        Return the SampleLostStatus of the reader

        SampleLostStatus has fields:
            total_count,
            total_count_change
            
        :rtype: SampleLostStatus
        '''
        self._check_handle()
        sample_lost_status = SampleLostStatus (0, 0, 0, 0)
        
        ret = self.rt.ddslib.dds_get_sample_lost_status (self.handle, byref(sample_lost_status))
        if ret < 0:
            raise DDSException('Failure retrieving sample_lost_status', ret)
        status = SampleLostStatus(
            sample_lost_status.total_count,
            sample_lost_status.total_count_change)
        return status