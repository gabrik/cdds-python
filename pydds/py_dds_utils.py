import xml.etree.ElementTree as ET
import subprocess
import struct
import enum
import re
from collections import OrderedDict, namedtuple

import os, sys

from pydds import *

from idl_parser import parser
from mesonbuild.msubprojects import foreach

import inspect


# constants
_MODULE_TAG      = 'module'
_TYPEDEF_TAG     = 'yypeDef'
_STRUCT_TAG      = 'struct'
_MEMBER_TAG      = 'member'
_ARRAY_TAG       = 'array'
_SEQUENCE_TAG    = 'sequence'
_TYPE_TAG        = 'type'
_STRING_TAG      = 'string'
_CHAR_TAG        = 'char'
_ENUM_TAG        = 'enum'
_ELEMENT_TAG     = 'element'

_NAME_ATTRIBUTE  = 'name'
_SIZE_ATTRIBUTE  = 'size'
_VALUE_ATTRIBUTE = 'value'

_MODULE_SEPARATOR = '::'

def _FoundTopic_Init(dp, topic_handle):
    foundTopic = FoundTopic(dp)
    foundTopic.handle = topic_handle
    return foundTopic

def _get_field_default(ele):
    if ele == _STRING_TAG:
        return ''
    elif ele == _SEQUENCE_TAG:
        return []
    elif ele == _ARRAY_TAG:
        array_size = int(ele.attrib[_SIZE_ATTRIBUTE])
        array_type = ele[0]
        return [_get_field_default(array_type) for _ in range(array_size)]
    elif ele == _TYPE_TAG:
        typename = ele.attrib[_NAME_ATTRIBUTE]
        actual_type = _get_actual_type(typename)
        if isinstance(actual_type, enum.EnumMeta):
            return actual_type(0)
        elif isinstance(actual_type, type):
            return actual_type()
        else:
            # it's a typedef, recurse...
            return _get_field_default(actual_type)
    elif ele == 'boolean':
        return False
    elif ele == 'char':
        return '\x00'
    elif ele in ('octet', 'short', 'long', 'longlong', 'ushort', 'ulong', 'ulonglong'):
        return 0
    elif ele in ('float', 'double'):
        return 0.0
    return None

class TopicDataClass(object):
    '''
    Abstract topic data class.
    Generated classes inherits this base class.
    '''

    def __init__(self, member_names = []):
        self._member_attributes = member_names
        self._typesupport = None
        self._nested_types = {}
        pass

    def get_vars(self):
        '''
        Return the dictionary of attribute and value pair for the topic data members.
        '''
        result = OrderedDict()
        return result

    def _format_list(self, list_val):
        result = []
        return result


def _create_class(name, members):
    ''' Create Python class based on an dictionary of members

        Args:
            name: name of the class to be created
            members (dict): name and type of properties
        Returns:
            dynamically created Python class
    '''
    
    def __init__(self, **kwargs):
        setattr(self, '_members', members)
        setattr(self, '_member_attributes', members.keys())
        member_names = []
        self._member_attributes = member_names
        # self._typesupport = None
        # _nested_types = {}

        # define variables with default value
        for member in members.keys():
            setattr(self, member, _get_field_default(members[member]))

        # set values for variables passed in
        for member_name, value in kwargs.items():
            setattr(self, member_name, value)
        
        for member in members.keys():
            self._member_attributes.append (member)
            
    def get_vars(self):
        result = OrderedDict()
        for member in self._member_attributes:
            result[member] = getattr(self, member)

        return result
    
    
    def gen_key(self):
        return self.userID
    
    def __eq__(self, other):
        result = ( type(other) == type(self) )
        if result:
            for member in self._members.keys():
                result = (getattr(self, member) == getattr(other, member) )
                if result == False :
                    break
            
        return result
    
    def _get_print_vars(self):
        result = []
        for key, val in self.get_vars().items():
            if isinstance(val, list):
                result.append("{}: [{}]".format(key, self._format_list(val)))
            else:
                result.append("{}: {}".format(key, val))
        return ', '.join(result)


    def __str__(self):
        res = self._get_print_vars()
        return res

    
    cls_name = name
    slots =list(members.keys())
    cls_attrs = {"__init__": __init__,
                 "gen_key": gen_key,
                 "__eq__": __eq__,
                 "__str__": __str__,
                 "_get_print_vars": _get_print_vars,
                 "get_vars" : get_vars
                 }
    
    # create topic data class
    data_class = type(cls_name, (TopicDataClass,), cls_attrs)
    return data_class
    

''' Create Python class based on a idl file

        Args:
            name: name of the class to be created
            idl_path: full path  of the idl file 
        Returns:
            dynamically created Python class
    '''
def create_class(class_name, idl_path):
    
    print("Generate {} from idl file".format(class_name))
    parser_ = parser.IDLParser()
    
    with open(idl_path, 'r') as idlf:
        contents = idlf.read()
        global_module = parser_.load( contents)
        
        for module in global_module.modules:
            
            mod_struct = module.structs
            for sub_str in mod_struct:
                member_dict = {}
                struct_complete_name = "{0}_{1}".format( module.name,sub_str.name)
                
                members = sub_str.members
                
                for member in members:
                    if( member.name not in member_dict):
                        member_dict[member.name] = _get_field_default(member.type.name)
                
                newClass = type(struct_complete_name, (object,), member_dict)
                
                other_new_class = _create_class (struct_complete_name, member_dict)
            
                X = newClass()
                variables = [i for i in dir(X) if i.find('__') == -1 ]
                
                other_X = other_new_class()
                variables = [i for i in dir(other_X) if i.find('__') == -1 ]
                
                return other_new_class
