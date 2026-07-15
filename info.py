from .checkHash import checkHash
from pathlib import Path
import json
def oreanInfo():
    changes,data = checkHash()
    repo = Path.cwd().name
    path = Path.cwd()
    version = "0.1.1"
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
    f=open(str(Path.cwd())+'\\.oreon\\commits\\latest\\changes\\metadata.json')
    d=json.loads(f.read())
    message_of_latest_commit=d['Message']
    date_created=d['Date_Created']
    f.close()
    tracked_files = len(data)
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
Total Commits     : {3}
Latest Commit     : "Latest"
Message           : {4}
Created           : {5}

WORKING TREE
────────────────────────────────────
Tracked Files     : {6}
Modified          : {7}
Added             : {8}
Deleted           : {9}
Status            : {10}

STORAGE
────────────────────────────────────
Commit Size       : {11}
Current Branch    : main""".format(repo,path,version,total_num,message_of_latest_commit,date_created,total_num,modified,Added,Deleted,dirty,total_size))
