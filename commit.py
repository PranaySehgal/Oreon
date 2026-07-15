from pathlib import Path
import os,json
import shutil
import uuid
import datetime
from .checkHash import checkHash
def commitData(message):
    path = str(Path.cwd())
    data = checkHash()
    changes = data[0]
    data = data[1]
    
    print(changes)
    f=open(path+"\\.oreon\\hashes.json",'w')
    f.write(json.dumps(data))
    f.close()
    if not len(os.listdir(path+'\\.oreon\\latest')):
        os.rmdir(path+'\\.oreon\\latest')
        os.mkdir(path+'\\.oreon\\commits\\latest')
        os.mkdir(path+'\\.oreon\\commits\\latest\\changes\\')
        f=open(path+'\\.oreon\\commits\\latest\\changes\\changes.json','w')
        f.write(json.dumps(changes))
        f.close()
        f=open(path+'\\.oreon\\commits\\latest\\changes\\metadata.json','w')
        f.write(json.dumps({
            "Message":message,
            "Date_Created":str(datetime.datetime.now())
        }))
        f.close()
        os.mkdir(path+'\\.oreon\\commits\\latest\\changes\\src')
    else:
        if changes=={}:
            print("No Changes Were Made")
            return 
        dir_name = str(uuid.uuid1())
        Path(path+'\\.oreon\\commits\\latest').rename(path+'\\.oreon\\commits\\'+dir_name)
        
        for i in changes:
            destination = Path(str(Path.cwd())+ '\\.oreon\\commits\\'+dir_name+'\\changes\\src\\'+i)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if changes[i][-1]=='updated' or changes[i][-1]=='deleted':
                shutil.copyfile(path+'\\.oreon\\latest\\'+i,destination)
            else:
                shutil.copyfile(path+"\\"+i,destination)
        f=open(path+'\\.oreon\\commits\\'+dir_name+'\\changes\\changes.json','w')
        f.write(json.dumps(changes))
        f.close()
        os.mkdir(path+'\\.oreon\\commits\\latest')
        os.mkdir(path+'\\.oreon\\commits\\latest\\changes\\')
        os.mkdir(path+'\\.oreon\\commits\\latest\\changes\\src\\')
        f=open(path+'\\.oreon\\commits\\latest\\changes\\metadata.json','w')
        f.write(json.dumps({
            "Message":message,
            "Date_Created":str(datetime.datetime.now())
        }))
        f.close()
        f=open(path+'\\.oreon\\commits\\latest\\changes\\changes.json','w')
        f.write("{}")
        f.close()
        shutil.rmtree(path+'\\.oreon\\latest')
    shutil.copytree(path,path+'\\.oreon\\latest',ignore=shutil.ignore_patterns(".oreon"))
