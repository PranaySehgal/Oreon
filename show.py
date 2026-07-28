from uuid import UUID
from pathlib import Path
from json import loads
from rich.console import Console
console = Console()
def oreonShow(branch,x):
    f = open(Path.cwd() / '.oreon' / 'branches.json','r')
    d=loads(f.read())
    f.close()
    
    f = open(Path.cwd() / '.oreon' / 'commits' / branch / str(x) / 'changes' / 'metadata.json','r')
    metadata=loads(f.read())
    f.close()
    console.print("""COMMIT {0}
────────────────────────

Message : {1}
""".format(x,metadata['Message']),style='bold green')
    added=[]
    deleted=[]
    modified=[]
    f = open(Path.cwd() / '.oreon' / 'commits' / branch / str(x) / 'changes' / 'changes.json','r')
    d=loads(f.read())
    f.close()
    for i in d:
        if i=='added':
            for j in d[i]:
                added.append(j)
        if i=='updated':
            for j in d[i]:
                modified.append(j)
        if i=='deleted':
            for j in d[i]:
                deleted.append(j)
    if added:
        added.insert(0,"Added")
    
    if deleted:
        deleted.insert(0,"Deleted")
    
    if modified:
        modified.insert(0,"Modified")
    
    for i in range(len(added)):
        if i==0:
            console.print(added[0],style='bold green')
            continue
        console.print("*\t"+added[i],style='bold green')
    for i in range(len(modified)):
        if i==0:
            console.print(modified[0],style='bold green')
            continue
        console.print("*\t"+modified[i],style='bold green')
    for i in range(len(deleted)):
        if i==0:
            console.print(deleted[0],style='bold green')
            continue
        console.print("*\t"+deleted[i],style='bold green')