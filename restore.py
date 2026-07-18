from pathlib import Path
from json import loads,dumps
import shutil,os
from .checkHash import  checkHash
def restore(commit_num,branches):
    for i in branches:
        if commit_num<=branches[i][-1]:
            if commit_num in branches[i]:
                break
    changes=loads(open(Path.cwd()/'.oreon'/'commits'/i/str(commit_num)/'changes'/'changes.json').read())
    for j in changes:
        if changes[j][1]=="updated" or changes[j][1]=="deleted":
            destination = Path.cwd() / changes[j][0]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(Path.cwd()/'.oreon'/'commits'/i/str(commit_num)/'changes'/'src'/changes[j][0],destination)
        else:
            if Path(str(Path.cwd())+"\\"+changes[j][0]).exists():
                os.remove(str(Path.cwd())+"\\"+changes[j][0])
def restoreCommit(x):
    for i in Path.cwd().iterdir():
        if i.name=='.oreon':
            continue
        elif i.is_dir():
            shutil.rmtree(i)
        elif i.is_file():
            i.unlink()
    f=open(str(Path.cwd())+'\\.oreon\\metadata.json','r')
    d=loads(f.read())
    cur_commit=d['last_commit']
    shutil.copytree(str(Path.cwd())+'\\.oreon\\latest\\',str(Path.cwd()),dirs_exist_ok=True)
    while cur_commit>int(x):
        restore(cur_commit,d['branches'])
        cur_commit-=1
    data = checkHash()[1]
    f=open(str(Path.cwd())+"\\.oreon\\hashes.json",'w')
    f.write(dumps(data))
    f.close()