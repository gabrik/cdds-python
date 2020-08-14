from .dds_binding import *
from .runtime import Runtime

from cdds import *
from ctypes import c_bool


class GaurdCondition (Entity):
    def __init__(self, entity):
        self.rt = Runtime.get_runtime()
        self.participant = entity.participant
        self.parent = entity

        self.handle = self.rt.ddslib.dds_create_guardcondition(entity.handle)

    def set_guard_condition(self, triggerd=True):
        ret = self.rt.ddslib.dds_set_guardcondition(self.handle, triggerd)
        if ret != 0:
            print("Error while executing set_gaurdcondition")

        return True

    def read_trigger(self):
        triggered = POINTER(c_bool)()
        ret = self.rt.ddslib.dds_read_guardcondition(self.handle, byref(triggered))

        if ret == 0:
            return triggered

        return None

    def take_trigger(self):
        triggered = POINTER(c_bool)()
        ret = self.rt.ddslib.dds_take_guardcondition(self.handle, byref(triggered))

        if ret == 0:
            return triggered

        return None

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
            raise Exception("Error while return loan, return code = {}".format(rc))

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
            raise Exception("Error while return loan, return code = {}".format(rc))
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
        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0:
            raise Exception("Error while return loan, return code = {}".format(rc))

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
            raise Exception("Error while return loan, return code = {}".format(rc))

        return data

    def lookup_instance(self, s):
        gk = self.keygen(s)

        kh = KeyHolder(gk)

        key = jsonpickle.encode(kh)
        value = jsonpickle.encode(s)

        sample = DDSKeyValue(key.encode(), value.encode())
        result = self.rt.ddslib.dds_lookup_instance(self.parent.handle, byref(sample))

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

        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0:
            raise Exception("Error while return loan, return code = {}".format(rc))

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

        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0:
            raise Exception("Error while return loan, return code = {}".format(rc))
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
            sp = cast(c_void_p(samples[i]), POINTER(DDSKeyValue))
            if infos[i].valid_data:
                si = infos[i]
                data.append(_Sample(jsonpickle.decode(sp[0].value.decode(encoding='UTF-8')), si))

        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0:
            raise Exception("Error while return loan, return code = {}".format(rc))
        return data
