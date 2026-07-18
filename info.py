from .checkHash import checkHash
from pathlib import Path
import json
def oreanInfo():
    changes = checkHash()[0]
    repo = Path.cwd().name
    path = Path.cwd()
    total_size=0
    total_num = 0
    commits = Path(Path.cwd() / ".oreon" / "commits")
    for item in commits.rglob("*"):
        if item.is_file():
            total_num+=1
            total_size+=(item.stat().st_size)
    units = ["B","KB","MB","GB","TB"]
    for unit in units:
        if total_size<1024 or unit == units[-1]:
            total_size = f'{total_size:.2f} {unit}'
            break
        total_size/=1024
    f = open(Path.cwd() / '.oreon' / 'metadata.json','r')
    d=json.loads(f.read())
    x=d['last_commit']
    version = d['version']
    d=d['branches']
    f.close()
    for i in d:
        if x<=d[i][-1]:
            break
    f=open(str(Path.cwd())+f'\\.oreon\\commits\\{i}\\{x}\\changes\\metadata.json')
    d=json.loads(f.read())
    message_of_latest_commit=d['Message']
    date_created=d['Date_Created']
    f.close()
    modified=0
    Added=0
    Deleted=0
    dirty="Dirty"
    for i in changes:
        if changes[i][-1] =='added':
            Added+=1
        elif changes[i][-1] =='updated':
            modified+=1
        elif changes[i][-1]=='deleted':
            Deleted+=1
    if not modified and not Deleted and not Added:
        dirty="Clean"
    print("""OREON REPOSITORY INFORMATION
────────────────────────────────────

Repository        : {0}
Root Path         : {1}
Oreon Version     : {2}

COMMITS
────────────────────────────────────
Total  Files      : {3}
Latest Commit     : Commit Number: {4}
Message           : {5}
Created           : {6}

WORKING TREE
────────────────────────────────────
Tracked Files     : {7}
Modified          : {8}
Added             : {9}
Deleted           : {10}
Status            : {11}

STORAGE
────────────────────────────────────
Commit Size       : {12}
Current Branch    : main""".format(repo,path,version,total_num,x,message_of_latest_commit,date_created,total_num,modified,Added,Deleted,dirty,total_size))
