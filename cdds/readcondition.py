from .dds_binding import *
import jsonpickle
from .runtime import Runtime

from cdds import *

from collections import namedtuple

_Sample = namedtuple('_Sample',['data','status'])

class ReadCondition (Entity):
    def __init__(self, reader, mask = all_samples()):
        self.rt = Runtime.get_runtime()
        self.participant = reader.participant
        self.parent = reader
        
        self.handle = self.rt.ddslib.dds_create_readcondition(reader.handle, mask)
        
        self.keygen = self.parent.topic.gen_key
        
    def get_mask(self):
        outMask = c_uint32(int('0xFFFFFFFF',16))
        retValue = self.rt.ddslib.dds_get_mask(self.handle, byref(outMask))
        if retValue != 0:
            raise Exception("Get_mask operation failed")
        return outMask
    
    def get_reader_handle (self):
        entity = self.rt.ddslib.dds_get_datareader(self.handle)
        
        if (entity < 0):
            raise Exception("readerCondition.get_reader operation failed")
        
        return entity
    
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
        if rc != 0 :
            raise Exception("Error while return loan, retuen code = {}".format(rc))
        
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
        if rc != 0 :
            raise Exception("Error while return loan, retuen code = {}".format(rc))
        
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
                
        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0 :
            raise Exception("Error while return loan, retuen code = {}".format(rc))
        
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
        
        return zip(data, infos)
    
    def lookup_instance (self, s):
        gk = self.keygen(s)
        
        kh = KeyHolder(gk)
        
        key = jsonpickle.encode(kh)
        value = jsonpickle.encode(s)
        
        sample = DDSKeyValue(key.encode(), value.encode())
        result = self.rt.ddslib.dds_lookup_instance(self.parent.handle, byref(sample))
        
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
        
        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0 :
            raise Exception("Error while return loan, retuen code = {}".format(rc))
        
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
        
        rc = self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        if rc != 0 :
            raise Exception("Error while return loan, retuen code = {}".format(rc))
        
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
                v = sp[0].value.decode(encoding='UTF-8')
                data.append(jsonpickle.decode(v))
#             else:
#                 kh = jsonpickle.decode(sp[0].key.decode(encoding='UTF-8'))
#                 data.append(kh)

        self.rt.ddslib.dds_return_loan(self.handle, samples, nr)
        return zip(data, infos)