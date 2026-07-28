import ctypes
import os
from json import dumps
from platform import system

from rich.console import Console

console = Console()
def __init__(path):
        os.makedirs('.oreon')
        os.makedirs('.oreon/latest')
        os.makedirs(path+'\\.oreon\\commits')
        os.makedirs(path+'\\.oreon\\commits\\main')
        with open(path+'\\.oreon\\hashes.json','w') as f:
            f.write("{}")
        with open(path+'/.oreonignore','w') as f:
            f.write("")
        with open(path+'\\.oreon\\metadata.json','w') as f:
            f.write(dumps({
                "cur_branch":"main",
                "version":"2.0.0",
                "ignore":[]
                }))
        with open(path+'\\.oreon\\branches.json','w') as f:
            f.write(dumps({
                "main":{
                    "Hierarchy":"",
                    "commits":[],
                    "next_commit":1,
                    "last_commit":None
                }
            }))
        
        if system()=='Windows':
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(path+"\\.oreon", FILE_ATTRIBUTE_HIDDEN)
        console.print("Directory Initialized Successfully",style='bold green')