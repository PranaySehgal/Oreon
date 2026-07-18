from .showCommits import showCommits
from uuid import UUID
from pathlib import Path
from json import loads
def oreonShow(x:int):
    f = open(Path.cwd() / '.oreon' / 'metadata.json','r')
    d=loads(f.read())['branches']
    f.close()
    for i in d:
        if int(x)<=d[i][-1]:
            break
    f = open(Path.cwd() / '.oreon' / 'commits' / i / str(x) / 'changes' / 'metadata.json','r')
    metadata=loads(f.read())
    f.close()
    print("""COMMIT {0}
────────────────────────

Message : {1}
""".format(x,metadata['Message']))
    added=[]
    deleted=[]
    modified=[]
    f = open(Path.cwd() / '.oreon' / 'commits' / i / str(x) / 'changes' / 'changes.json','r')
    d=loads(f.read())
    f.close()
    for i in d:
        if d[i][-1] =='added':
            added.append(d[i][0])
        elif d[i][-1] =='updated':
            modified.append(d[i][0])
        elif d[i][-1] =='deleted':
            deleted.append(d[i][0])
    if added:
        added.insert(0,"Added")
    
    if deleted:
        deleted.insert(0,"Deleted")
    
    if modified:
        modified.insert(0,"Modified")
    
    for i in range(len(added)):
        if i==0:
            print(added[0])
            continue
        print("*\t",added[i])
    for i in range(len(modified)):
        if i==0:
            print(modified[0])
            continue
        print("*\t",modified[i])
    for i in range(len(deleted)):
        if i==0:
            print(deleted[0])
            continue
        print("*\t",deleted[i])