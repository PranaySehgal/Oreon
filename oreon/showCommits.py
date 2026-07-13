import os
from json import loads
from pathlib import Path
import tabulate
from .restore import restoreCommit
def showCommits():
    path = str(Path.cwd())
    directory = os.listdir(path+'\\.oreon\\commits\\')
    metadata=[['Serial Number','Message','Date Created']]
    index=1
    for i in directory:
        d = open(path+'\\.oreon\\commits\\'+i+'\\changes\\metadata.json')
        f=d.read()
        f = loads(f)
        d.close()
        metadata.append([index,f['Message']  if f['Message'] else "No Commit Message",f['Date_Created']])
        index+=1
    print(tabulate.tabulate(metadata,tablefmt="fancy_grid"))
    length= len(metadata)-1
    x=input("Enter the serial number of the commit you want to restore....")
    if not x.isdigit() or int(x)>length or int(x)<1:
        print("Invalid Input")
        return
    else:
        restoreCommit(directory[int(x)-1])
        