import os
from platform import system
import ctypes
def __init__(path):
        os.makedirs('.oreon')
        os.makedirs(path+'\\.oreon\\commits')
        os.makedirs(path+'\\.oreon\\latest')
        f=open(path+'\\.oreon\\hashes.json','w')
        f.write("{}")
        f.close()
        f=open(path+'\\.oreon\\changes.json','w')
        f.close()
        
        if system()=='Windows':
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(path+"\\.oreon", FILE_ATTRIBUTE_HIDDEN)