from .dds_binding import *

class Policy:
    def __init__(self, id, kind):
        self.id = id
        self.kind = kind
        
class Deadline (Policy):
    def __init__(self, deadline = 0 ):
        Policy.__init__(self, DDS_DEADLINE_QOS_POLICY_ID, deadline )
        self.deadline = deadline
        

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


class ResourceLimit(Policy):
    def __init__(self, max_instances = LENGTH_UNLIMITED , max_samples = LENGTH_UNLIMITED, max_samples_per_instance = LENGTH_UNLIMITED):
        Policy.__init__(self, DDS_RESOURCELIMITS_QOS_POLICY_ID, None)
        self.max_instances = max_instances
        self.max_samples = max_samples 
        self.max_samples_per_instance = max_samples_per_instance


DDS_V_State = [Reliable(), KeepLastHistory(1), Volatile(), ManualInstanceDispose(), SourceTimestampOrder()]
DDS_TL_State = [Reliable(), KeepLastHistory(1), TransientLocal(), ManualInstanceDispose(), SourceTimestampOrder()]
DDS_State = DDS_V_State

DDS_Event = [Reliable(), KeepAllHistory(), ManualInstanceDispose(), SourceTimestampOrder()]
