import os, sys

from idl_parser import parser

parser_ = parser.IDLParser()

# idl_str = """
# module my_module {
#   struct Time {
#     long sec;
#     long usec;
#   };
#   struct Msg
#   {
#     long userID;
#     string message;
#   };
# 
#   typedef sequence<double> DoubleSeq;
#   
#   struct TimedDoubleSeq {
#     Time tm;
#     DoubleSeq data;
#   };
# 
#   enum RETURN_VALUE {
#     RETURN_OK,
#     RETURN_FAILED,
#   };
# 
#   interface DataGetter {
#     RETURN_VALUE getData(out TimedDoubleSeq data);
#   };
# 
# };
# """
#     
# global_module = parser_.load(idl_str)
# my_module = global_module.module_by_name('my_module')
# dataGetter = my_module.interface_by_name('DataGetter')
# print ('DataGetter interface')
# for m in dataGetter.methods:
#   print ('- method:')
#   print ('  name:', m.name)
#   print ('  returns:', m.returns.name)
#   print ('  arguments:')
#   for a in m.arguments:
#     print ('    name:', a.name)
#     print ('    type:', a.type)
#     print ('    direction:', a.direction)
#     
# doubleSeq = my_module.typedef_by_name('DoubleSeq')
# print ('typedef %s %s' % (doubleSeq.type.name, doubleSeq.name))
# 
# timedDoubleSeq = my_module.struct_by_name('TimedDoubleSeq')
# print ('TimedDoubleSeq')
# for m in timedDoubleSeq.members:
#   print ('- member:')
#   print ('  name:', m.name)
#   print ('  type:', m.type.name)
#   
#   
# MsgSeq = my_module.struct_by_name('Msg')
# print ('Msg')
# for m in timedDoubleSeq.members:
#   print ('- member:')
#   print ('  name:', m.name)
#   print ('  type:', m.type.name)        
  
idl_path = '/home/firas/cyclone/cdds_python/lexer/lexer.idl'

  
with open(idl_path, 'r') as idlf:
    
    contents = idlf.read()
    print(contents)
    global_module = parser_.load( contents)
    
    my_module = global_module.module_by_name('my_module')
    print ('my_module')
    
    for m in my_module.modules:
        print ('- module:')
        print ('  name:', m.name)
        
    for m in my_module.structs:
        print ('- structs:')
        print ('  name:', m.name)
        # attrs.update({m.name: m.type.name})
    
    
    dataGetter = my_module.interface_by_name('DataGetter')
    print ('DataGetter interface')
    for m in dataGetter.methods:
      print ('- method:')
      print ('  name:', m.name)
      print ('  returns:', m.returns.name)
      print ('  arguments:')
      for a in m.arguments:
        print ('    name:', a.name)
        print ('    type:', a.type)
        print ('    direction:', a.direction)
        
    doubleSeq = my_module.typedef_by_name('DoubleSeq')
    print ('typedef %s %s' % (doubleSeq.type.name, doubleSeq.name))
    
    timedDoubleSeq = my_module.struct_by_name('TimedDoubleSeq')
    print ('TimedDoubleSeq')
    for m in timedDoubleSeq.members:
        print ('- member:')
        print ('  name:', m.name)
        print ('  type:', m.type.name)
      
      
    MsgSeq = my_module.struct_by_name('Msg')
    print ('Msg')
    for m in MsgSeq.members:
        print ('- member:')
        print ('  name:', m.name)
        print ('  type:', m.type.name)
      
    MsgSeq = my_module.struct_by_name('Inner')
    print ('Inner')
    for m in MsgSeq.members:
        print ('- member:')
        print ('  name:', m.name)
        print ('  type:', m.type.name)
        
        
    MsgSeq = my_module.struct_by_name('SequenceOfStruct_struct')
    print ('SequenceOfStruct_struct')
    for m in MsgSeq.members:
        print ('- member:')
        print ('  name:', m.name)
        print ('  type:', m.type.name)
        # attrs.update({m.name: m.type.name})
        
#     SequenceOfStruct = type('SequenceOfStruct_struct', (object,), {})
#     print(type(SequenceOfStruct))
#     
#     newSeq = SequenceOfStruct()
#     print(type(newSeq))


      
   
        
    my_sub_module = my_module.module_by_name('module_NestedStruct')
    
    MsgSeq = my_sub_module.struct_by_name('NestedStruct_struct')
    print ('NestedStruct_struct')
    for m in MsgSeq.members:
        print ('- member:')
        print ('  name:', m.name)
        print ('  type:', m.type.name)
        # attrs.update({m.name: m.type.name})

    doubleSeq = my_sub_module.typedef_by_name('other_inner_struct')
    print ('typedef %s %s' % (doubleSeq.type.name, doubleSeq.name))
    
    
      
      
    MsgSeq = my_sub_module.struct_by_name('NestedStruct_struct')
    print ('NestedStruct_struct')
    for m in MsgSeq.members:
        print ('- member:')
        print ('  name:', m.name)
        print ('  type:', m.type.name)
      
    MsgSeq = my_sub_module.struct_by_name('other_Inner')
    print ('other_Inner')
    for m in MsgSeq.members:
        print ('- member:')
        print ('  name:', m.name)
        print ('  type:', m.type.name)
        
        
    MsgSeq = my_module.struct_by_name('SequenceOfStruct_struct')
    print ('SequenceOfStruct_struct')
    for m in MsgSeq.members:
        print ('- member:')
        print ('  name:', m.name)
        print ('  type:', m.type.name)
        # attrs.update({m.name: m.type.name})
        
#     SequenceOfStruct = type('SequenceOfStruct_struct', (object,), {})
#     print(type(SequenceOfStruct))
#     
#     newSeq = SequenceOfStruct()
#     print(type(newSeq))


      
    MsgSeq = my_sub_module.struct_by_name('NestedStruct_struct')
    print ('NestedStruct_struct')
    for m in MsgSeq.members:
        print ('- member:')
        print ('  name:', m.name)
        print ('  type:', m.type.name)
        # attrs.update({m.name: m.type.name})
        
        