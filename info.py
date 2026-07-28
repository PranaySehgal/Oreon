from .checkHash import checkHash
from pathlib import Path
from rich.console import Console

import json
console = Console()
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
    f = open(Path.cwd() / '.oreon' / 'branches.json','r')
    d=json.loads(f.read())
    branches=list(d.keys())
    f.close()
    f = open(Path.cwd() / '.oreon' / 'metadata.json','r')
    d=json.loads(f.read())
    version = d['version']
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
    console.print("""OREON REPOSITORY INFORMATION
────────────────────────────────────

Repository        : {0}
Root Path         : {1}
Oreon Version     : {2}

COMMITS
────────────────────────────────────

Total  Files      : {3}
Branches          : {4}
WORKING TREE

────────────────────────────────────

Tracked Files     : {5}
Modified          : {6}
Added             : {7}
Deleted           : {8}
Status            : {9}

STORAGE
────────────────────────────────────

Commit Size       : {10}
Current Branch    : main""".format(repo,path,version,total_num,branches,total_num,modified,Added,Deleted,dirty,total_size),style='bold green')
