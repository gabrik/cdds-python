import platform
import os
from ctypes import *

class Topic_Support :
    def __init__(self, domainParticipant, topic_descriptor ):
        self.rt = Runtime.get_runtime()
        self.domainParticipant = domainParticipant
        
        self.size = 0
        self.align = ''
        self.flag = 0
        self.typename = ''
        self.keys = []
        self.nops = 0
        self.ops = []
        self.meta = ''
        
    
        
        