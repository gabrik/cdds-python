from ctypes import *
from .dds_binding import *
the_runtime = None

class Runtime:
    @staticmethod
    def get_runtime():
        global the_runtime
        if the_runtime is not None:
            return the_runtime
        else:
            the_runtime = Runtime()
            return the_runtime

    def __init__(self):
        self.dataListenerMap = {}
        self.subscriptionMatchedListenerMap = {}
        self.livelinessChangeListenerMap = {}

        self.ddslib = CDLL(cham_lib_path)
        self.stublib = CDLL(bit_lib_path)
        self.helloworld_lib = CDLL(helloworld_lib_path)

        self.kv_topic = None
        self.v_topic = None
        # -- Entity Operations --
        self.ddslib.dds_delete.restype = dds_return_t
        self.ddslib.dds_delete.argtypes = [dds_entity_t]
        
        self.ddslib.dds_enable.restype = dds_return_t
        self.ddslib.dds_enable.argtypes = [dds_entity_t]
        # -- Participant Operations --
        self.ddslib.dds_create_participant.restype = dds_entity_t
        self.ddslib.dds_create_participant.argtypes = [dds_domainid_t, dds_qos_p_t, dds_listener_p_t]

        self.ddslib.dds_get_parent.restype = dds_entity_t
        self.ddslib.dds_get_parent.argtypes = [dds_entity_t]

        self.ddslib.dds_get_participant.restype = dds_entity_t
        self.ddslib.dds_get_participant.argtypes = [dds_entity_t]

        # -- Topic Operations --
        self.ddslib.dds_create_topic.restype = dds_entity_t
        self.ddslib.dds_create_topic.argtypes = [dds_entity_t, dds_topic_descriptor_p_t, c_char_p, dds_qos_p_t, dds_listener_p_t]

        self.ddslib.dds_find_topic.restype = dds_entity_t
        self.ddslib.dds_find_topic.argtypes = [dds_entity_t, c_char_p]
        
        self.ddslib.dds_get_name.restype = dds_return_t
        self.ddslib.dds_get_name.argtypes = [dds_entity_t, c_char_p, c_int]

        # -- Publisher / Subscriber Operations --

        self.ddslib.dds_create_publisher.restype = dds_entity_t
        self.ddslib.dds_create_publisher.argtypes = [dds_entity_t, dds_qos_p_t, dds_listener_p_t]

        self.ddslib.dds_create_subscriber.restype = dds_entity_t
        self.ddslib.dds_create_subscriber.argtypes = [dds_entity_t, dds_qos_p_t, dds_listener_p_t]

        self.ddslib.dds_get_subscriber.restype = dds_entity_t
        self.ddslib.dds_get_subscriber.argtypes = [dds_entity_t]

        self.ddslib.dds_get_publisher.restype = dds_entity_t
        self.ddslib.dds_get_publisher.argtypes = [dds_entity_t]

        # -- Reader  / Writer Operations --
        self.ddslib.dds_create_reader.restype = dds_entity_t
        self.ddslib.dds_create_reader.argtypes = [dds_entity_t, dds_entity_t, dds_qos_p_t, dds_listener_p_t]

        self.ddslib.dds_lookup_instance.restype = dds_instance_handle_t
        self.ddslib.dds_lookup_instance.argtypes = [dds_entity_t, c_void_p]

        self.ddslib.dds_reader_wait_for_historical_data.restype = dds_return_t
        self.ddslib.dds_reader_wait_for_historical_data.argtypes = [dds_entity_t, dds_duration_t]

        self.ddslib.dds_get_datareader.restype = dds_entity_t
        self.ddslib.dds_get_datareader.argtypes = [dds_entity_t]

        self.ddslib.dds_wait_for_acks.restype = dds_return_t
        self.ddslib.dds_wait_for_acks.argtypes = [dds_entity_t, dds_duration_t]

        self.ddslib.dds_create_writer.restype = dds_entity_t
        self.ddslib.dds_create_writer.argtypes = [dds_entity_t, dds_entity_t, dds_qos_p_t, dds_listener_p_t]

        # -- QoS operations --
        self.ddslib.dds_create_qos.restype = dds_qos_p_t
        self.ddslib.dds_create_qos.argtypes = []

        self.ddslib.dds_delete_qos.restype = None
        self.ddslib.dds_delete_qos.argtypes = [dds_qos_p_t]

        self.ddslib.dds_qset_durability.restype = None
        self.ddslib.dds_qset_durability.argtypes = [dds_qos_p_t, c_uint32]

        self.ddslib.dds_qset_history.restype = None
        self.ddslib.dds_qset_history.argtypes = [dds_qos_p_t, c_uint32, c_uint32]

        self.ddslib.dds_qset_reliability.restype = None
        self.ddslib.dds_qset_reliability.argtypes = [dds_qos_p_t, c_uint32, c_uint64]

        self.ddslib.dds_qset_ownership.restype = None
        self.ddslib.dds_qset_ownership.argtypes = [dds_qos_p_t, c_uint32]

        self.ddslib.dds_qset_ownership_strength.restype = None
        self.ddslib.dds_qset_ownership_strength.argtypes = [dds_qos_p_t, c_uint32]

        self.ddslib.dds_qset_destination_order.restype = None
        self.ddslib.dds_qset_destination_order.argtypes = [dds_qos_p_t, c_uint32]
        
        self.ddslib.dds_qget_durability.restype = c_bool
        self.ddslib.dds_qget_durability.argtypes = [dds_qos_p_t, c_uint32]

        # -- read / take --
        self.ddslib.dds_take.restype = c_int
        self.ddslib.dds_take.argtypes = [dds_entity_t, POINTER(c_void_p), POINTER(SampleInfo), c_size_t, c_uint32]

        self.ddslib.dds_read.restype = c_int
        self.ddslib.dds_read.argtypes = [dds_entity_t, POINTER(c_void_p), POINTER(SampleInfo), c_size_t, c_uint32]

        self.ddslib.dds_read_mask.restype = c_int
        self.ddslib.dds_read_mask.argtypes = [dds_entity_t, POINTER(c_void_p), POINTER(SampleInfo), c_size_t, c_uint32, c_uint32]

        self.ddslib.dds_take_mask.restype = c_int
        self.ddslib.dds_take_mask.argtypes = [dds_entity_t, POINTER(c_void_p), POINTER(SampleInfo), c_size_t, c_uint32,
                                              c_uint32]
        # -- read / take with loan--
        self.ddslib.dds_read_wl.restype = c_int
        self.ddslib.dds_read_wl.argtypes = [dds_entity_t, POINTER(c_void_p), POINTER(SampleInfo), c_uint32]
        
        self.ddslib.dds_read_mask_wl.restype = c_int
        self.ddslib.dds_read_mask_wl.argtypes = [dds_entity_t, POINTER(c_void_p), POINTER(SampleInfo), c_uint32, c_uint32]
        
        self.ddslib.dds_read_instance.restype = c_int
        self.ddslib.dds_read_instance.argstypes = [dds_entity_t, POINTER(c_void_p), POINTER(SampleInfo), c_uint32, c_uint32, dds_instance_handle_t]
        
        self.ddslib.dds_take_mask_wl.restype = c_int
        self.ddslib.dds_take_mask_wl.argtypes = [dds_entity_t, POINTER(c_void_p), POINTER(SampleInfo), c_uint32, c_uint32]

        self.ddslib.dds_return_loan.restype = c_int
        self.ddslib.dds_return_loan.argtypes = [dds_entity_t, POINTER(c_void_p), c_size_t]

        self.ddslib.dds_take_next.restype = c_int
        self.ddslib.dds_take_next.argtypes = [dds_entity_t, POINTER(c_void_p), POINTER(SampleInfo)]

        self.ddslib.dds_read_next.restype = c_int
        self.ddslib.dds_read_next.argtypes = [dds_entity_t, POINTER(c_void_p), POINTER(SampleInfo)]

        # -- dispoase --
        self.ddslib.dds_dispose.restype = dds_return_t
        self.ddslib.dds_dispose.argtypes = [dds_entity_t, c_void_p]

        self.ddslib.dds_dispose.restype = dds_return_t
        self.ddslib.dds_dispose.argtypes = [dds_entity_t, c_void_p]

        self.ddslib.dds_write.restype = dds_return_t
        self.ddslib.dds_write.argtypes = [dds_entity_t, c_void_p]

        # -- Waitset Operations --
        # create
        self.ddslib.dds_create_waitset.restype = dds_entity_t
        self.ddslib.dds_create_waitset.argtypes = [dds_entity_t]

        # attach / detach
        self.ddslib.dds_waitset_attach.restype = dds_return_t
        self.ddslib.dds_waitset_attach.argtypes = [dds_entity_t, dds_entity_t, dds_attach_t]

        self.ddslib.dds_waitset_detach.restype = dds_return_t
        self.ddslib.dds_waitset_detach.argtypes = [dds_entity_t, dds_entity_t]

        # wait
        self.ddslib.dds_waitset_wait.restype = dds_return_t
        self.ddslib.dds_waitset_wait.argtypes = [dds_entity_t, POINTER(dds_attach_t), c_size_t, dds_duration_t]

        # -- Condition Operations --
        self.ddslib.dds_create_readcondition.restype = dds_entity_t
        self.ddslib.dds_create_readcondition.argtypes = [dds_entity_t, c_uint32]

        self.ddslib.dds_create_querycondition.restype = dds_entity_t
        self.ddslib.dds_create_querycondition.argtypes = [dds_entity_t, c_uint32, CFUNCTYPE(c_bool, c_void_p)]
        
        self.ddslib.dds_create_guardcondition.restype = dds_entity_t
        self.ddslib.dds_create_guardcondition.argstypes = [dds_entity_t]
        
        self.ddslib.dds_get_mask.restype = dds_return_t
        self.ddslib.dds_get_mask.argstypes = [dds_entity_t, c_void_p]
        
        self.ddslib.dds_get_datareader.restype = dds_entity_t
        self.ddslib.dds_get_datareader.argstypes = [dds_entity_t]
        self.ddslib.dds_set_guardcondition.restype = dds_return_t
        self.ddslib.dds_set_guardcondition.argstypes = [dds_entity_t, c_bool]
        
        self.ddslib.dds_read_guardcondition.restype = dds_return_t
        self.ddslib.dds_read_guardcondition.argstypes = [dds_entity_t, POINTER(c_bool)]
        
        self.ddslib.dds_take_guardcondition.restype = dds_return_t
        self.ddslib.dds_take_guardcondition.argstypes = [dds_entity_t, POINTER(c_bool)]

        # -- Listeners --
        self.ddslib.dds_create_listener.restype = dds_listener_p_t
        self.ddslib.dds_create_listener.argtypes = [c_void_p]

        self.ddslib.dds_delete_listener.restype = None
        self.ddslib.dds_delete_listener.argtypes = [dds_listener_p_t]

        self.ddslib.dds_lset_data_available.restype = None
        self.ddslib.dds_lset_data_available.argtypes = [dds_listener_p_t, DATA_AVAILABLE_PROTO]

        self.ddslib.dds_lset_liveliness_changed.restype = None
        self.ddslib.dds_lset_liveliness_changed.argtypes = [dds_listener_p_t, LIVELINESS_CHANGED_PROTO]

        self.ddslib.dds_lset_subscription_matched.restype = None
        self.ddslib.dds_lset_subscription_matched.argtypes = [dds_listener_p_t, SUBSCRIPTION_MATCHED_PROTO]

        self.ddslib.dds_alloc.restype = c_void_p
        self.ddslib.dds_alloc.argtypes = [c_size_t]

        self.ddslib.dds_free.restype = None
        self.ddslib.dds_free.argtypes = [c_void_p]

        global the_runtime
        the_runtime = self

    def register_data_listener(self, handle, fun):
        h = repr(handle)
        self.dataListenerMap[h] = fun

    def register_liveliness_changed_listener(self, handle, fun):
        h = repr(handle)
        self.livelinessChangeListenerMap[h] = fun

    def register_subscription_matched_listener(self, handle, fun):
        h = repr(handle)
        self.subscriptionMatchedListenerMap[h] = fun

    @staticmethod
    def dispatch_data_listener(handle):
        h = repr(handle)
        the_runtime = Runtime.get_runtime()
        if h in the_runtime.dataListenerMap:
            fun = the_runtime.dataListenerMap[h]
            fun(handle)

    @staticmethod
    def dispatch_subscription_matched_listener(handle, s):
        h = repr(handle)
        the_runtime = Runtime.get_runtime()
        if h in the_runtime.subscriptionMatchedListenerMap:
            fun = the_runtime.subscriptionMatchedListenerMap[h]
            fun(handle, s)

    @staticmethod
    def dispatch_liveliness_changed_listener(handle, s):
        h = repr(handle)
        the_runtime = Runtime.get_runtime()
        if h in the_runtime.livelinessChangeListenerMap:
            fun = the_runtime.livelinessChangeListenerMap[h]
            fun(handle, s)


    def get_key_value_type_support(self):
        return self.stublib.dds_bit_SKeySValue_desc

    def get_simple_value_type_support(self):
        return self.stublib.dds_bit_SValue_desc
    def get_hello_world_key_value_type_support(self):
        return self.helloworld_lib.HelloWorldDataMsg_keys

    def get_hello_world_simple_value_type_support(self):
        return self.helloworld_lib.HelloWorldData_Msg_desc

    def to_rw_qos(self, ps):
        if ps is None:
            return None

        qos = self.create_dds_qos()

        for p in ps:
            if p.id == DDS_DURABILITY_QOS_POLICY_ID:
                self.ddslib.dds_qset_durability(qos, p.kind)
            elif p.id == DDS_HISTORY_QOS_POLICY_ID:
                self.ddslib.dds_qset_history(qos, p.kind, p.depth)
            elif p.id == DDS_RELIABILITY_QOS_POLICY_ID:
                self.ddslib.dds_qset_reliability(qos, p.kind, p.max_blocking_time)
            elif p.id == DDS_OWNERSHIP_QOS_POLICY_ID:
                self.ddslib.dds_qset_ownership(qos, p.kind)
                if p.kind == DDS_OWNERSHIP_EXCLUSIVE:
                    self.ddslib.dds_qset_ownership_strength(qos, p.strength)
            elif p.id == DDS_WRITERDATALIFECYCLE_QOS_POLICY_ID:
                self.ddslib.dds_qset_writer_data_lifecycle(qos, p.auto_dispose)
            elif p.id == DDS_DESTINATIONORDER_QOS_POLICY_ID:
                self.ddslib.dds_qset_destination_order(qos, p.kind)
        return qos


    def to_ps_qos(self, ps):
        if ps is None:
            return None

        qos = self.create_dds_qos()
        xs = list(filter(lambda p: p.id == DDS_PARTITION_QOS_POLICY_ID, ps))

        if len(xs) > 0:
            policy = xs[0]
            L = len(policy.partitions)
            vec = (c_char_p * L)()
            sbuf = list(map(lambda s: s.encode(), policy.partitions))
            vec[:] = sbuf
            self.ddslib.dds_qset_partition(qos, c_uint32(L), vec)
        return qos

    def create_dds_qos(self):
        return c_void_p(self.ddslib.dds_create_qos())

    def release_dds_qos(self, qos):
        self.ddslib.dds_delete_qos(qos)


    def close(self):
        # Magic value is DDS_CYCLONEDDS_HANDLE, so this tears down
        # the entire Cyclone run-time in a supported way once that
        # bit is merged in. Until then, there is no supported way.
        self.ddslib.dds_delete(2147418368)