from .runtime import Runtime
from ctypes import *
from cdds import *


class Entity(object):
    def __init__(self):
        self.rt = Runtime.get_runtime()
        self._handle = None
        self._parent = None
        self._qos = None
        self._listener = None

        self._participant = None
        self.enabled = True

    def enable(self):
        self.enabled = True
        rc = self.rt.ddslib.dds_enable(self.handle)
        return rc

    def delete(self):
        rc = self.rt.ddslib.dds_delete()
        return rc

    def get_participant(self):
        participant = None
        if(self._handle is not None):
            participant = self.rt.ddslib.dds_get_participant(self.handle)
        return participant

    def get_children(self, size=0):
        rc = 0
        childern = {}
        rc = self.rt.ddslib.dds_get_children(self.handle, childeren, size)

        if rc > 0:
            return childern
        return rc

    def set_qos(self, qos=[]):
        rc = 0
        rc = self.rt.ddslib.dds_set_qos(self.handle, self.qos)
        return rc

    def get_qos(self):
        rc = 0
        qos_policies = []
        rc = self.rt.ddslib.dds_get_qos(self.handle, qos_policies)

        if(rc == 0):
            return qos_policies
        else:
            return rc

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent_entity):
        self._parent = parent_entity

    @property
    def participant(self):
        return self._participant

    @participant.setter
    def participant(self, entity):
        if (entity is not None):
            self._participant = entity

    @property
    def qos(self):
        return self._qos

    @qos.setter
    def qos(self, qos):
        rc = qos
        return rc

    @property
    def handle(self):
        return self._handle

    @handle.setter
    def handle(self, entity):
        self._handle = entity

    @handle.deleter
    def handle(self):
        self.rt.ddslib.dds_delete(self._handle)

    def _check_handle(self):
        if self.handle is None:
            raise Exception('Entity is already closed')
