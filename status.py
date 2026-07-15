from .checkHash import checkHash
from pathlib import Path
def oreanStatus():
    repo = Path.cwd().name
    print(f"""
          OREON STATUS
────────────────────────
Repository : {repo}
Branch     : main
""")
    modified=[]
    deleted=[]
    added=[]
    dirty = "Dirty"
    changes=checkHash()[0]
    for i in changes:
        if changes[i][-1]=='added':
            added.append("A\t"+i)
        elif changes[i][-1]=='updated':
            modified.append("M\t"+i)
        elif changes[i][-1]=='deleted':
            deleted.append("D\t"+i)
    
    if  not len(modified) and not len(deleted) and not len(added):
        print("No Changes Were Made")
        dirty="Clean"
        print(f"Working Tree: {dirty}") 
        return
    else:
        if len(added):
            added.insert(0,f'Added Files ({len(added)})')
        
        if len(modified):
            modified.insert(0,f'Modified Files ({len(modified)})')
        
        if len(deleted):
            deleted.insert(0,f'Deleted Files ({len(deleted)})')
        
    for i in added:
        print(i)
    if len(added):
        print()
    for i in modified:
        print(i)
    if len(modified):
        print()
    for i in deleted:
        print(i)
    if len(deleted):
        print()
    print(f"Working Tree: {dirty}") 