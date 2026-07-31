from json import loads
from pathlib import Path

from rich.console import Console

console = Console()
def oreonShow(branch,x):
    with open(Path.cwd() / '.oreon' / 'branches.json','r') as f:
        d=loads(f.read())
    
    with open(Path.cwd() / '.oreon' / 'commits' / branch / str(x) / 'changes' / 'metadata.json','r') as f:
        metadata=loads(f.read())
    console.print("""COMMIT {}
────────────────────────

Message : {}
""".format(x,metadata['Message']),style='bold green')
    added=[]
    deleted=[]
    modified=[]
    with open(Path.cwd() / '.oreon' / 'commits' / branch / str(x) / 'changes' / 'changes.json','r') as f:
        d=loads(f.read())
    for i in d:
        if i=='added':
            for j in d[i]:
                added.append(j)  # noqa: PERF402
        if i=='updated':
            for j in d[i]:
                modified.append(j)  # noqa: PERF402
        if i=='deleted':
            for j in d[i]:
                deleted.append(j)  # noqa: PERF402
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