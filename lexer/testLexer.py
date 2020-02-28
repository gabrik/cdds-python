from idl_parser import parser
import pydds.py_dds_utils as utils



# def _get_field_default(ele):
#     if ele.tag == _STRING_TAG:
#         return ''
#     elif ele.tag == _SEQUENCE_TAG:
#         return []
#     elif ele.tag == _ARRAY_TAG:
#         array_size = int(ele.attrib[_SIZE_ATTRIBUTE])
#         array_type = ele[0]
#         return [_get_field_default(array_type) for _ in range(array_size)]
#     elif ele.tag == _TYPE_TAG:
#         typename = ele.attrib[_NAME_ATTRIBUTE]
#         actual_type = _get_actual_type(typename)
#         if isinstance(actual_type, enum.EnumMeta):
#             return actual_type(0)
#         elif isinstance(actual_type, type):
#             return actual_type()
#         else:
#             # it's a typedef, recurse...
#             return _get_field_default(actual_type)
#     elif ele.tag == 'boolean':
#         return False
#     elif ele.tag == 'char':
#         return '\x00'
#     elif ele.tag in ('octet', 'short', 'long', 'longlong', 'ushort', 'ulong', 'ulonglong'):
#         return 0
#     elif ele.tag in ('float', 'double'):
#         return 0.0
#     return None

def _get_field_default(ele):
    if ele == utils._STRING_TAG:
        return ''
    elif ele == utils._SEQUENCE_TAG:
        return []
    elif ele == utils._ARRAY_TAG:
        array_size = int(ele.attrib[_SIZE_ATTRIBUTE])
        array_type = ele[0]
        return [_get_field_default(array_type) for _ in range(array_size)]
    elif ele == utils._TYPE_TAG:
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

def _create_class(name, members):
    ''' Create python class given data members

        Args:
            name(string): name of the class
            members(dict): name and type of properties
        Returns:
            dynamically created python class
    '''
    def __init__(self, **kwargs):

        setattr(self, '_members', members)
        setattr(self, '_member_attributes', members.keys())

        # define variables with default value
        for member in members.keys():
            setattr(self, member, _get_field_default(members[member]))

        # set values for variables passed in
        for key, value in kwargs.items():
            if key not in members:
                raise TypeError("Invalid argument name : %s" %(key))
            setattr(self, key, value)

    cls_name = name
    slots =list(members.keys())
    slots.append("_members")
    slots.append("__dict__")
    cls_attrs = {"__init__": __init__,
                 "__slots__": slots,
                 "get_vars": get_vars,}
    
    # create topic data class
    data_class = type(cls_name, (object,), cls_attrs)
    return data_class
    

def handle_idl_module ():
    pass
    

    
def create_class(class_name, idl_path):
    print("Create class begins here")
    idl_path = './lexer/lexer.idl'
    parser_ = parser.IDLParser()
    
    
    
    with open(idl_path, 'r') as idlf:
        contents = idlf.read()
        global_module = parser_.load( contents)
        
        for module in global_module.modules:
            print('Module is ', module.name)
            
            mod_struct = module.structs
            #sub_mods = dic['modules']
            print('sub struucts are')
            for sub_str in mod_struct:
                member_dict = {}
                # print("{0}_{1}".format( module.name,sub_str.name) )
                
                struct_complete_name = "{0}_{1}".format( module.name,sub_str.name)
                
                members = sub_str.members
                
                for member in members:
                    print("Type of ", member.name," is ", str(member.type.name) )
                    
                    if( member.name not in member_dict):
                        member_dict[member.name] = _get_field_default(member.type.name)
                
                print(struct_complete_name)
                
                # module_complete_name = module.name + '_' + sub_m.name
                #print('complete name', module_complete_name)
                
#                 member_dict.update({
#                     '__repr__': reprfun,
#                     '__str__': reprfun,
#                     })
                
                
                
                newClass = type(struct_complete_name, (object,), member_dict)
            
                print(type(newClass))
                X = newClass()
#                 print(type(X))
                print('X is ',X)
#                 print(X.__dir__())
                dir(X)
                variables = [i for i in dir(X) if i.find('__') == -1 ]
                
                print('Attributes are ',variables)
            
            
    

idl_path = './lexer/lexer.idl'

create_class("", idl_path)
