import os,shutil
from json import loads
from pathlib import Path
import tabulate
from .restore import restoreCommit
def showCommits():
    path = str(Path.cwd())
    f=open(Path.cwd()/'.oreon'/'metadata.json','r')
    d = loads(f.read())
    f.close()
    index=1
    metadata=[['Serial Number','Message','Date Created']]
    for i in d['branches']:
        l = os.listdir(f"{path}/.oreon/commits/{i}")
        for j in l:
            file=open(f"{path}\\.oreon\\commits\\{i}\\{j}\\changes\\metadata.json")
            data=file.read()
            data = loads(data)
            file.close()
            metadata.append([index,data['Message']  if data['Message'] else "No Commit Message",data['Date_Created']])
            index+=1
    print(tabulate.tabulate(metadata,tablefmt="fancy_grid"))
    length= len(metadata)-1
    return length