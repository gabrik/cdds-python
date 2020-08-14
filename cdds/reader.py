from .dds_binding import *
import jsonpickle
from .runtime import Runtime

from cdds import *

from collections import namedtuple

_Sample = namedtuple('_Sample', ['data', 'status'])


@LIVELINESS_CHANGED_PROTO
def trampoline_on_liveliness_changed(r, s, a):
    # print("[python-cdds]:>>  Dispatching Liveliness change")
    Runtime.dispatch_liveliness_changed_listener(r, s)


@DATA_AVAILABLE_PROTO
def trampoline_on_data_available(r, a):
    # print("[python-cdds]:>>  Dispatching Data Available ")
    Runtime.dispatch_data_listener(r)


@SUBSCRIPTION_MATCHED_PROTO
def trampoline_on_subscription_matched(e, s, a):
    # print("[python-cdds]:>>  Dispatching Subscription Match")
    Runtime.dispatch_subscription_matched_listener(e, s)


@SAMPLE_LOST_PROTO
def trampoline_on_sample_lost(e, s, a):
    # print("[python-cdds]:>>  Dispatching Sample Lost")
    global logger
    logger.debug('DefaultListener', '>> Sample Lost')


def do_nothing(a):
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
    def __init__(self, sub, topic, ps=None, data_listener=None):
        self.rt = Runtime.get_runtime()
        self.participant = sub.participant
        self.parent = sub
        self.topic = topic

        self.keygen = self.topic.gen_key

        qos = self.rt.to_rw_qos(ps)

        self._qos = qos

        if data_listener is None:
            self.data_listener = do_nothing
        else:
            self.data_listener = data_listener

        self.listener_handle = self.rt.ddslib.dds_create_listener(None)
        self.rt.ddslib.dds_lset_data_available(self.listener_handle, trampoline_on_data_available)
        self.rt.ddslib.dds_lset_liveliness_changed(self.listener_handle, trampoline_on_liveliness_changed)
        self.rt.ddslib.dds_lset_subscription_matched(self.listener_handle, trampoline_on_subscription_matched)
        self.handle = self.rt.ddslib.dds_create_reader(sub.handle, self.topic.handle, self.qos, self.listener_handle)
        assert (self.handle > 0)
#         self.rt.register_data_listener(self.handle, self.__handle_data)

    @property
    def handle(self):
        return super(Reader, self).handle

    @handle.setter
    def handle(self, entity):
        super(Reader, self.__class__).handle.fset(self, entity)

    @property
    def participant(self):
        return super(Reader, self).participant

    @participant.setter
    def participant(self, entity):
        super(Reader, self.__class__).participant.fset(self, entity)

    @property
    def qos(self):
        return super(Reader, self).qos

    @qos.setter
    def qos(self, qos):
        super(Reader, self.__class__).qos.fset(self, qos)

    def on_data_available(self, fun):
        self.data_listener = fun

    def on_subscription_matched(self, fun):
        self.subsciption_listener = fun
        self.rt.register_subscription_matched_listener(self.handle, self.__handle_sub_matched)

    def on_liveliness_changed(self, fun):
        self._liveliness_listener = fun
        self.rt.register_liveliness_changed_listener(self.handle, self.__handle_liveliness_change)

    def __handle_data(self, r):
        self.data_listener(self)

    def __handle_sub_matched(self, r, s):
        self.subsciption_listener(self, s)

    def __handle_liveliness_change(self, r, s):
        self._liveliness_listener(self, s)

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
        nr = self.rt.ddslib.dds_read(self.handle, samples, infos, MAX_SAMPLES, MAX_SAMPLES)
        if nr < 0:
            raise Exception("Read n = {0} operation failed".format(nr))
        data = []
        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
            if infos[i].valid_data:

                si = infos[i]
                data.append(_Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8')), si))

        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0:
            raise Exception("Read_instance exception whlie return loan rc = {0} operation failed".format(nr))
        return data

    def read_mask(self, mask):
        ivec = (SampleInfo * MAX_SAMPLES)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * MAX_SAMPLES)()

        nr = self.rt.ddslib.dds_read_mask(self.handle, samples, infos, MAX_SAMPLES, MAX_SAMPLES, mask)
        if nr < 0:
            raise Exception("Read n = {0} operation failed".format(nr))

        data = []

        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
            if infos[i].valid_data:
                si = infos[i]
                data.append(_Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8')), si))
        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0:
            raise Exception("Read_instance exception whlie return loan rc = {0} operation failed".format(nr))
        return data

    def read_n(self, n):
        ivec = (SampleInfo * n)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * n)()

        nr = self.rt.ddslib.dds_read(self.handle, samples, infos, n, n)

        if nr < 0:
            raise Exception("Read n = {0} operation failed".format(nr))

        data = []
        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))

            if infos[i].valid_data:
                si = infos[i]
                data.append(_Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8')), si))

        return data

    def read_wl(self):
        ivec = (SampleInfo * MAX_SAMPLES)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * MAX_SAMPLES)()
        nr = self.rt.ddslib.dds_read_wl(self.handle, samples, infos, MAX_SAMPLES, MAX_SAMPLES)

        if nr < 0:
            raise Exception("Read operation with loan failed, return code is {0}".format(nr))

        data = []

        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
            if infos[i].valid_data:
                si = infos[i]
                data.append(_Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8')), si))

        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)

        if rc != 0:
            raise Exception("Error while return loan, retuen code = {}".format(rc))

        return data

    def lookup_instance(self, s):
        gk = self.keygen(s)

        kh = KeyHolder(gk)

        key = jsonpickle.encode(kh)
        value = jsonpickle.encode(s)

        sample = DDSKeyValue(key.encode(), value.encode())
        result = self.rt.ddslib.dds_lookup_instance(self.handle, byref(sample))

        print("result ", result)
        return result

    def read_instance(self, instacne_handle):
        ivec = (SampleInfo * MAX_SAMPLES)()
        infos = cast(ivec, POINTER(SampleInfo))
        samples = (c_void_p * MAX_SAMPLES)()

        nr = self.rt.ddslib.dds_read_instance(self.handle, samples, infos, MAX_SAMPLES, MAX_SAMPLES, c_uint64(instacne_handle))

        if nr < 0:
            raise Exception("Read n = {0} operation failed".format(nr))

        data = []

        for i in range(nr):
            sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
            if infos[i].valid_data:

                si = infos[i]
                data.append(_Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8')), si))

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
                    si = infos[i]
                    data.append(_Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8')), si))
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
                    si = infos[i]
                    data.append(_Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8')), si))
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
                    si = infos[i]
                    data.append(_Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8')), si))
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
                    si = infos[i]
                    data.append(_Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8')), si))
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
                si = infos[i]
                data.append(_Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8')), si))

        self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        return data

    def wait_history(self, timeout):
        return self.rt.ddslib.dds_reader_wait_for_historical_data(self.handle, timeout)
