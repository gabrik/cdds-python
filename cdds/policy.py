from .dds_binding import *


class Policy:
    def __init__(self, id, kind=0):
        self._id = id
        self._kind = kind

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id and self.kind == other.kind
        return False

    @property
    def kind(self):
        return self._kind

    @property
    def id(self):
        return self._id

    @kind.setter
    def kind(self, value):
        self._kind = value

    @id.setter
    def id(self, value):
        self._id = value

class DurabilityQoSPolocy(Policy):
    def __init__(self, kind=DDS_DURABILITY_VOLATILE, depth = 0):
        Policy.__init__(self, DDS_DURABILITY_QOS_POLICY_ID, kind)
        self._depth = depth
        
    @property
    def depth(self):
        return self._depth
    
    @depth.setter
    def depth(self, new_depth):
        if new_depth <0:
            self._depth = 0
        else:
            self._depth = new_depth

class HistoryQosPolicy(Policy):
    def __init__(self, kind = DDS_HISTORY_KEEP_LAST, depth=1):
        Policy.__init__(self, DDS_HISTORY_QOS_POLICY_ID, DDS_HISTORY_KEEP_LAST)
        self._depth = depth
    
    @property
    def depth(self):
        return self._depth
    
    @depth.setter
    def depth(self, depth):
        if depth < 0:
            self._depth = 1
        self._depth = depth

class ResourceLimitsQosPolicy(Policy):
    def __init__(self, max_samples = LENGTH_UNLIMITED, max_instances = LENGTH_UNLIMITED, max_samples_per_instance = LENGTH_UNLIMITED):
        Policy.__init__(self, DDS_RESOURCELIMITS_QOS_POLICY_ID, None)
        self._max_samples = max_samples
        self._max_instances =  max_instances
        self._max_samples_per_instance = max_samples_per_instance
    
    @property
    def max_samples (self): 
        return self._max_samples
    
    @max_samples.setter
    def max_samples(self, max_samples):
        if max_samples <= 0:
            self._max_samples =LENGTH_UNLIMITED
        else:
            self._max_samples = max_samples
            
    @property
    def max_instances(self):
        return max_instances
    
    @max_instances.setter
    def max_instances(self, max_instances):
        if max_instances <= 0:
            self._max_instances = LENGTH_UNLMITED
        else:
            self._max_instances = max_instances
    
    @property
    def max_samples_per_instance(self):
        return self._max_samples_per_instance
    
    @max_samples_per_instance.setter
    def max_samples_per_instance(self, max_samples_per_instance):
        if max_samples_per_instance <=0:
            self._max_samples_per_instance = LENGTH_UNLIMITED
        else:
            self._max_samples_per_instance = max_samples_per_instance
            
    
class PresentationQosPolicy (Policy):
    def __init__(self, kind=DDS_PRESENTATION_INSTANCE, coherent_access = False, ordered_access = False):
        Policy.__init__(self, DDS_PRESENTATION_QOS_POLICY_ID, kind)
        self._coherent_access = coherent_access
        self._ordered_access = ordered_access
        
    @property
    def ordered_access(self):
        return self._ordered_access
    
    @ordered_access.setter
    def ordered_access(self, ordered_access = False):
        self._ordered_access = ordered_access
        
        
    @property
    def coherent_access(self):
        return self._coherent_access
    
    @coherent_access.setter
    def coherent_access(self, coherent_access = False):
        self._coherent_access = coherent_access

class LifespanQosPolicy(Policy):
    def __init__(self, lifespan = dds_infinity()):
        Policy.__init__(self, DDS_LIFESPAN_QOS_POLICY_ID, None)
        self._lifesapn = lifespan
        
    @property
    def lifespan(self):
        return self._lifesapn
    
    @lifespan.setter
    def lifespan(self, lifespan = dds_infinity()):
        self._lifesapn = lifespan
        
class DeadlineQosPolicy(Policy):
    def __init__(self, deadline = dds_infinity()):
        Policy.__init__(self, DDS_DEADLINE_QOS_POLICY_ID)
        self._deadline = deadline
        
    @property
    def deadline(self):
        return self._deadline
    
    @deadline.setter
    def deadline(self, deadline ):
        self._deadline = deadline
    
class LatencyBudgetQosPolicy(Policy):
    def __init__(self, duration):
        Policy.__init__(self, DDS_LATENCYBUDGET_QOS_POLICY_ID, None)
    
class OwnershipQosPolicy(Policy):
    def __init__(self, id, kind=DDS_OWNERSHIP_SHARED):
        Policy.__init__(self, DDS_OWNERSHIP_QOS_POLICY_ID, kind)
        
class OwnershipStrengthQosPolicy(Policy):
    def __init__(self, value = 0):
        Policy.__init__(self, DDS_OWNERSHIPSTRENGTH_QOS_POLICY_ID, None)
        self._value = value
        
    @property
    def value (self):
        return self._value
    
    @ value.setter
    def value(self, value = 0):
        self._value = value
        
    

class LivelinessQosPolicy(Policy):
    def __init__(self, kind = DDS_LIVELINESS_AUTOMATIC, lease_duration = dds_infinity()):
        Policy.__init__(self, DDS_LIVELINESS_QOS_POLICY_ID, kind)
        self._lease_duration = lease_duration
        
    @property
    def lease_duration(self):
        return self._lease_duration
    
    @lease_duration.setter
    def lease_duration(self, duration = dds_infinity()):
        self._lease_duration = duration

class TimeBasedFilterQosPolicy(Policy):
    def __init__(self, minimum_separation = 0):
        Policy.__init__(self, DDS_TIMEBASEDFILTER_QOS_POLICY_ID, None)
        self._minimum_sepration = minimum_separation
        
    @property
    def minimum_sepration(self):
        return self._minimum_sepration
    
    @minimum_sepration.setter
    def minimum_sepration(self, minimum_sepration = 0):
        self._minimum_sepration = minimum_sepration
        
class PartitionQosPolicy(Policy):
    def __init__(self, partition):
        Policy.__init__(self, DDS_PARTITION_QOS_POLICY_ID, None)
        self._partition = partition
    
    @property
    def partition(self):
        return self._partition
    
    @partition.setter
    def partition(self, partition):
        self._partition = partition
        
class ReliabilityQosPolicy(Policy):
    def __init__(self, kind = DDS_RELIABILITY_BEST_EFFORT, max_blocking_time = dds_nanos( 100000000) ):
        Policy.__init__(self, DDS_RELIABILITY_QOS_POLICY_ID, kind)
        self._max_blocking_time = max_blocking_time
        
    @property
    def max_blocking_time(self):
        return self._max_blocking_time
    
    @max_blocking_time.setter
    def max_blocking_time(self, max_blocking_time):
        self._max_blocking_time = max_blocking_time

class TransportPriorityQosPolicy(Policy):
    def __init__(self, value = 0):
        Policy.__init__(self, DDS_TRANSPORTPRIORITY_QOS_POLICY_ID, None)
        self._value = value
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        
class DestinationOrderQosPolicy(Policy):
    def __init__(self, kind = DDS_DESTINATIONORDER_BY_SOURCE_TIMESTAMP):
        Policy.__init__(self, DDS_DESTINATIONORDER_QOS_POLICY_ID, kind)
        
class WriterDataLifecycleQosPolicy(Policy):
    def __init__(self, autodispose_unregistered_instances = True):
        Policy.__init__(self, DDS_LIVELINESS_QOS_POLICY_ID, None)
        self._autodispose_unregistered_instances = autodispose_unregistered_instances
        
    @property
    def autodispose_unregistered_instances(self):
        return self._autodispose_unregistered_instances
    
    @autodispose_unregistered_instances.setter
    def autodispose_unregistered_instances(self, autodispose_unregistered_instances= True):
        self._autodispose_unregistered_instances = autodispose_unregistered_instances
    
class ReaderDataLifecycleQosPolicy(Policy):
    def __init__(self, autopurge_nowriter_samples = dds_infinity(), autopurge_disposed_samples_delay = dds_infinity()):
        Policy.__init__(self, DDS_READERDATALIFECYCLE_QOS_POLICY_ID, None)
        self._autopurge_nowriter_samples = autopurge_nowriter_samples
        self._autopurge_disposed_samples_delay = autopurge_disposed_samples_delay
        
    @property
    def autopurge_nowriter_samples(self):
        return self._autopurge_nowriter_samples
    
    @autopurge_nowriter_samples.setter
    def autopurge_nowriter_samples(self, autopurge_nowriter_samples = dds_infinity()):
        self._autopurge_nowriter_samples = autopurge_nowriter_samples
        
    @property
    def autopurge_disposed_samples_delay(self):
        return self._autopurge_disposed_samples_delay
    
    @autopurge_disposed_samples_delay.setter
    def autopurge_disposed_samples_delay(self, autopurge_disposed_samples_delay = dds_infinity()):
        self._autopurge_disposed_samples_delay = autopurge_disposed_samples_delay
        

class DurabilityServiceQosPolicy(Policy):
    def __init__(self, service_cleanup_delay = 0, history_kind = DDS_HISTORY_KEEP_LAST,
                 history_depth = 1, max_samples = LENGTH_UNLIMITED,
                 max_instances = LENGTH_UNLIMITED,
                 max_samples_per_instance = LENGTH_UNLIMITED):
        Policy.__init__(self, DDS_DURABILITYSERVICE_QOS_POLICY_ID, kind)
        self._service_cleanup_delay = service_cleanup_delay
        self._history_kind = history_kind
        self._history_depth = history_depth
        self._max_samples = max_samples
        self._max_instances = max_instances
        self._max_samples_per_instance = max_samples_per_instance
        
    @property
    def service_cleanup_delay(self):
        return self._service_cleanup_delay
    @service_cleanup_delay.setter
    def service_cleanup_delay(self, service_cleanup_delay):
        self._service_cleanup_delay = service_cleanup_delay
        
    @property
    def history_kind(self):
        return _history_kind
    
    @history_kind.setter
    def history_kind(self, history_kind):
        self._history_kind = history_kind
        
    @property
    def history_depth(self):
         return self._history_depth
     
    @history_depth.setter
    def history_depth(self, history_depth):
        self._history_depth = history_depth
        
    @property
    def max_samples(self):
        return self._max_samples
    
    @max_samples.setter
    def max_samples(self, max_samples):
        self._max_samples = max_samples
        
    @property
    def max_instances(self):
        return self._max_instances
    
    @max_instances.setter
    def max_instances(self, max_instances):
        self._max_instances = max_instances
        
    @property
    def max_samples_per_instance(self):
        return self._max_samples_per_instance
    
    @max_samples_per_instance.setter
    def max_samples_per_instance(self, max_samples_per_instance):
        self._max_samples_per_instance = max_samples_per_instance
         
         
    
class UserdataQosPolicy(Policy):
    def __init__(self, value):
        Policy.__init__(self, DDS_USERDATA_QOS_POLICY_ID, None)
        self._value = value
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        
class TopicdataQosPolicy(Policy):
    def __init__(self, value = ''):
        Policy.__init__(self, DDS_TOPICDATA_QOS_POLICY_ID, None)
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        
        
class GroupdataQosPolicy(Policy):
    def __init__(self, value = ''):
        Policy.__init__(self, DDS_GROUPDATA_QOS_POLICY_ID, None)
        self._value = value
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value 
        
        
class Partition(Policy):
    def __init__(self, ps):
        Policy.__init__(self, DDS_PARTITION_QOS_POLICY_ID, None)
        self.partitions = ps


class Reliable(Policy):
    def __init__(self, blocking_time = 0):
        Policy.__init__(self, DDS_RELIABILITY_QOS_POLICY_ID, DDS_RELIABILITY_RELIABLE)
        self.max_blocking_time = blocking_time


class BestEffort(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_RELIABILITY_QOS_POLICY_ID, DDS_RELIABILITY_BEST_EFFORT)
        self.max_blocking_time = 0


class KeepLastHistory(Policy):
    def __init__(self, depth):
        Policy.__init__(self, DDS_HISTORY_QOS_POLICY_ID, DDS_HISTORY_KEEP_LAST)
        self.depth = depth


class KeepAllHistory(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_HISTORY_QOS_POLICY_ID, DDS_HISTORY_KEEP_ALL)
        self.depth = 0


class Volatile(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_DURABILITY_QOS_POLICY_ID, DDS_DURABILITY_VOLATILE)


class TransientLocal(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_DURABILITY_QOS_POLICY_ID, DDS_DURABILITY_TRANSIENT_LOCAL)


class Transient(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_DURABILITY_QOS_POLICY_ID,  DDS_DURABILITY_TRANSIENT)


class Persistent(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_DURABILITY_QOS_POLICY_ID, DDS_DURABILITY_PERSISTENT)


class ExclusiveOwnership(Policy):
    def __init__(self, strength):
        Policy.__init__(self, DDS_OWNERSHIP_QOS_POLICY_ID, DDS_OWNERSHIP_EXCLUSIVE)
        self.strength = strength


class SharedOwnership(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_OWNERSHIP_QOS_POLICY_ID, DDS_OWNERSHIP_SHARED)


class ManualInstanceDispose(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_WRITERDATALIFECYCLE_QOS_POLICY_ID, None)
        self.auto_dispose = False


class AutoInstanceDispose(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_WRITERDATALIFECYCLE_QOS_POLICY_ID, None)
        self.auto_dispose = True


class ReceptionTimestampOrder(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_DESTINATIONORDER_QOS_POLICY_ID, DDS_DESTINATIONORDER_BY_RECEPTION_TIMESTAMP)

class SourceTimestampOrder(Policy):
    def __init__(self):
        Policy.__init__(self, DDS_DESTINATIONORDER_QOS_POLICY_ID, DDS_DESTINATIONORDER_BY_SOURCE_TIMESTAMP)



DDS_V_State = [Reliable(), KeepLastHistory(1), Volatile(), ManualInstanceDispose(), SourceTimestampOrder()]
DDS_TL_State = [Reliable(), KeepLastHistory(1), TransientLocal(), ManualInstanceDispose(), SourceTimestampOrder()]
DDS_State = DDS_V_State

DDS_Event = [Reliable(), KeepAllHistory(), ManualInstanceDispose(), SourceTimestampOrder()]
