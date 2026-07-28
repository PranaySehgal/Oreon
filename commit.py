import datetime
import shutil
from getpass import getuser
from json import dumps, loads
from os import mkdir, remove
from pathlib import Path
from uuid import uuid1

from rich.console import Console

from .checkHash import checkHash

console = Console()
def commitData(message):
    path = str(Path.cwd())
    ignore=[]
    with open(path+'\\.oreon\\metadata.json','r') as f:
        d=loads(f.read())
    cur_branch = d['cur_branch']
    ignore=d['ignore']
    if Path(path+'/.oreonignore').exists():
        with open(path+'/.oreonignore','r',encoding='UTF-8') as f:
            ignoreFiles=f.read().split()
        ignore=[]
        for i in ignoreFiles:
            ignore.append(str(i))
        with open(path+'\\.oreon\\metadata.json','w') as f:
            d['ignore']=ignore
            f.write(dumps(d))
        ignore=d['ignore']
    updated,added,deleted,data = checkHash()
    changes = {"updated":updated,"added":added,"deleted":deleted}
    with open(path+"\\.oreon\\hashes.json",'w') as f:
        f.write(dumps(data))
    if not (added or updated or deleted) and message!='CB1011MERGECOMMIT':
        console.print("No Changes Were Made",style='bold cyan')
        if Path(path+'/.oreonignore').exists():
            remove(path+'/.oreonignore')
        return
    with open(Path.cwd()/'.oreon'/'branches.json') as f:
        d = loads(f.read())
    dir_name =  d[cur_branch]['next_commit']
    d[cur_branch]['next_commit']+=1
    d[cur_branch]['last_commit']=dir_name
    d[cur_branch]['commits'].append(dir_name)
    with open(Path.cwd()/'.oreon'/'branches.json','w') as f:
        f.write(dumps(d))
    for i in added:
        destination = Path(str(Path.cwd())+ f'\\.oreon\\commits\\{cur_branch}\\{dir_name}\\changes\\src\\'+i)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path.cwd()/i,destination)
    for i in deleted:
        destination = Path(str(Path.cwd())+ f'\\.oreon\\commits\\{cur_branch}\\{dir_name}\\changes\\src\\'+i)
        destination.parent.mkdir(parents=True, exist_ok=True)
        Path(Path.cwd()/'.oreon'/'latest'/i).parent.mkdir(parents=True, exist_ok=True)
        if Path(Path.cwd()/'.oreon'/'latest'/i).exists():
            shutil.copyfile(Path.cwd()/'.oreon'/'latest'/i,destination)
    for i in updated:
        destination = Path(str(Path.cwd())+ f'\\.oreon\\commits\\{cur_branch}\\{dir_name}\\changes\\src\\'+i)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path.cwd()/i,destination)
    if not Path(Path.cwd()/'.oreon'/'commits'/cur_branch/str(dir_name)/'changes/').exists():
        
        mkdir(Path.cwd()/'.oreon'/'commits'/cur_branch/str(dir_name))
        mkdir(Path.cwd()/'.oreon'/'commits'/cur_branch/str(dir_name)/'changes/')
        
    with open(path+f'\\.oreon\\commits\\{cur_branch}\\{dir_name}\\changes\\changes.json','w') as f:
        f.write(dumps(changes))
    with open(path+f'\\.oreon\\commits\\{cur_branch}\\{dir_name}\\changes\\metadata.json','w') as f:
        f.write(dumps({
            "Author":getuser(),
            "Message":message,
            "Date_Created":str(datetime.datetime.now()),  # noqa: DTZ005
            "Random_Id":str(uuid1())
        }))
    if Path(Path.cwd()/'.oreon'/'latest').exists():
        shutil.rmtree(Path.cwd()/'.oreon'/'latest')
    shutil.copytree(Path.cwd(),Path.cwd()/'.oreon'/'latest',ignore=shutil.ignore_patterns('.oreon',*ignore)) 
    console.print("Changes Published Successfully",style='bold green')
    if Path(path+'/.oreonignore').exists():
        remove(path+'/.oreonignore')