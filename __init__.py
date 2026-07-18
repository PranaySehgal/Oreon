import os
from platform import system
import ctypes
from json import dumps
def __init__(path):
        os.makedirs('.oreon')
        os.makedirs(path+'\\.oreon\\commits')
        os.makedirs(path+'\\.oreon\\commits\\main')
        os.makedirs(path+'\\.oreon\\latest')
        f=open(path+'\\.oreon\\hashes.json','w')
        f.write("{}")
        f.close()
        f=open(path+'\\.oreon\\metadata.json','w')
        f.write(dumps({
            "cur_branch":"main",
            "next_file_name":1,
            "branches":{
                "main":[]
            },
            "version":"1.0.0"
            }))
        f.close()
        f=open(path+'\\.oreon\\changes.json','w')
        f.close()
        
        if system()=='Windows':
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(path+"\\.oreon", FILE_ATTRIBUTE_HIDDEN)