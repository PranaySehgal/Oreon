from pathlib import Path
from json import loads,dumps
import shutil,os
from rich.console import Console
from .checkHash import  checkHash
from time import sleep
console = Console()
def restore(branch,commit_num,ignore):
    folder = list(Path(Path.cwd()/'.oreon'/'commits'/branch).iterdir())
    if Path(Path.cwd()/'.oreon'/'commits'/branch/'base').exists():
        shutil.copytree(Path.cwd()/'.oreon'/'commits'/branch/'base'/'changes'/'src',Path.cwd()/'.oreon'/'commits'/branch/'temp',ignore=shutil.ignore_patterns("metadata.json"))
    else:
        if not Path(Path.cwd()/'.oreon'/'commits'/branch/'temp').exists():
            os.mkdir(Path.cwd()/'.oreon'/'commits'/branch/'temp')
    if commit_num=='CB1011':
        pass
    else:
        array=[]
        for i in folder:
            if i.is_dir():
                if i.name=='base':
                    continue
                if int(i.name)==int(commit_num)+1:
                    break
                with open(Path.cwd()/'.oreon'/'commits'/branch/i/'changes'/'changes.json') as f:
                    d=loads(f.read())
                modified=d['updated']
                deleted=d['deleted']
                added=d['added']
                f.close()
                for j in modified:
                    destination = Path(Path.cwd()/'.oreon'/'commits'/branch/'temp'/j)
                    destination.parent.mkdir(parents=True,exist_ok=True)
                    os.remove(Path.cwd()/'.oreon'/'commits'/branch/'temp'/j)
                    array.append(str(j))
                    shutil.copy(Path.cwd()/'.oreon'/'commits'/branch/i/'changes'/'src'/j,Path.cwd()/'.oreon'/'commits'/branch/'temp'/j)
                for j in deleted:
                    array.remove(str(j))
                    os.remove(Path.cwd()/'.oreon'/'commits'/branch/'temp'/j)
                for j in added:
                    array.append(str(j))
                    destination = Path(Path.cwd()/'.oreon'/'commits'/branch/'temp'/j)
                    destination.parent.mkdir(parents=True,exist_ok=True)
                    
                    shutil.copy(i/'changes'/'src'/j,Path.cwd()/'.oreon'/'commits'/branch/'temp'/j)
    for i in Path.cwd().rglob("*"):
        source = str(i.relative_to(Path.cwd()))
        ignoreFiles = False
        for j in ignore:
            if str(j) == source:
                ignoreFiles=True
                break
        if i.name=='.oreon' or ignoreFiles or '.oreon' in str(i):
            continue
        elif i.is_dir():
            shutil.rmtree(i)
        elif i.is_file():
            i.unlink()
    shutil.copytree(Path.cwd()/'.oreon'/'commits'/branch/'temp/',Path.cwd(),dirs_exist_ok=True)
    shutil.copytree(Path.cwd()/'.oreon'/'commits'/branch/'temp/',Path.cwd()/'.oreon'/'latest',dirs_exist_ok=True)
    shutil.rmtree(Path.cwd()/'.oreon'/'commits'/branch/'temp')
def restoreCommit(commit_num,branch=None,preview=False):
    with open(str(Path.cwd())+'\\.oreon\\metadata.json','r') as f:
        d=loads(f.read())
    cur_branch=d['cur_branch']
    ignore = d['ignore']
    f.close()
    if preview:
        shutil.copytree(Path.cwd(),Path.cwd()/'.oreon'/cur_branch/'Recovery',ignore=shutil.ignore_patterns(".oreon"))
    restore(cur_branch if not branch else branch,commit_num,ignore)
    if preview:
        x=input("Hey! We have restored the commit According to your will. It will stay in your parent directory for a specific period and will be changed to the original data after that. Kindly enter the time for which you want to keep this data (In Seconds)")
        if not x.isdigit():
            console.print("Invalid Input.  Restoring Original Repo Immediately",style='bold red')
        else:
            sleep(float(x))
        for i in Path.cwd().rglob("*"):
            ignoreFiles=False
            source = i.relative_to(Path.cwd())
            for j in ignore:
                if str(j)==source:
                    ignoreFiles=True
                    break
            if '.oreon' in str(i) or i.name=='.oreon' or ignoreFiles:
                continue
            elif i.is_file():
                i.unlink()
            else:
                shutil.rmtree(i)
        
        shutil.copytree(Path.cwd()/'.oreon'/cur_branch/'Recovery',Path.cwd(),dirs_exist_ok=True)
        shutil.rmtree(Path.cwd()/'.oreon'/cur_branch/'Recovery')
    
    data = checkHash()[-1]
    with open(str(Path.cwd())+"\\.oreon\\hashes.json",'w') as f: 
        f.write(dumps(data))
    f.close()