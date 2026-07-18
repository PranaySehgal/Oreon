from pathlib import Path
import os,json
import shutil
import datetime
from .checkHash import checkHash
def commitData(message):
    path = str(Path.cwd())
    data = checkHash()
    changes = data[0]
    data = data[1]
    f=open(path+"\\.oreon\\hashes.json",'w')
    f.write(json.dumps(data))
    f.close()
    f=open(path+'\\.oreon\\metadata.json','r')
    d=json.loads(f.read())
    dir_name =  d['next_file_name']
    d['next_file_name']+=1
    d['last_commit']=dir_name
    cur_branch = d['cur_branch']
    d["branches"][cur_branch].append(dir_name)
    f.close()
    if changes=={}:
        print("No Changes Were Made")
        return
    f=open(path+'\\.oreon\\metadata.json','w')
    f.write(json.dumps(d))
    f.close()
    for i in changes:
        destination = Path(str(Path.cwd())+ f'\\.oreon\\commits\\{cur_branch}\\{dir_name}\\changes\\src\\'+i)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if changes[i][-1]=='updated' or changes[i][-1]=='deleted':
            shutil.copyfile(path+'\\.oreon\\latest\\'+i,destination)
        else:
            shutil.copyfile(path+"\\"+i,destination)
    f=open(path+f'\\.oreon\\commits\\{cur_branch}\\{dir_name}\\changes\\changes.json','w')
    f.write(json.dumps(changes))
    f.close()
    f=open(path+f'\\.oreon\\commits\\{cur_branch}\\{dir_name}\\changes\\metadata.json','w')
    f.write(json.dumps({
        "Message":message,
        "Date_Created":str(datetime.datetime.now())
    }))
    f.close()
    shutil.rmtree(path+'\\.oreon\\latest')
    shutil.copytree(path,path+'\\.oreon\\latest',ignore=shutil.ignore_patterns(".oreon"))