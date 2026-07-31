import json
from pathlib import Path

from rich.console import Console

from .checkHash import checkHash

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
    with open(Path.cwd() / '.oreon' / 'branches.json','r') as f:
        d=json.loads(f.read())
    branches=list(d.keys())
    with open(Path.cwd() / '.oreon' / 'metadata.json','r') as f:
        d=json.loads(f.read())
    version = d['version']
    current_branch = d.get('cur_branch', 'main')
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
    console.print(f"""OREON REPOSITORY INFORMATION
────────────────────────────────────

Repository        : {repo}
Root Path         : {path}
Oreon Version     : {version}

COMMITS
────────────────────────────────────

Total  Files      : {total_num}
Branches          : {branches}
WORKING TREE

────────────────────────────────────

Tracked Files     : {total_num}
Modified          : {modified}
Added             : {Added}
Deleted           : {Deleted}
Status            : {dirty}

STORAGE
────────────────────────────────────

Commit Size       : {total_size}
Current Branch    : {current_branch}""",style='bold green')
