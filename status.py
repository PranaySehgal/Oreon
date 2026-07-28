from .checkHash import checkHash
from pathlib import Path
from rich.console import Console
console = Console()
def oreanStatus():
    repo = Path.cwd().name
    console.print(f"""
          OREON STATUS
────────────────────────
Repository : {repo}
Branch     : main
""",style='bold green')
    modified=[]
    deleted=[]
    added=[]
    dirty = "Dirty"
    modifiedChanges,addedChanges,deletedChanges=checkHash()[:-1]
    for i in addedChanges:
            added.append("A\t"+i)
    for i in deletedChanges:
            deleted.append("D\t"+i)
    for i in modifiedChanges:
            modified.append("M\t"+i)
    
    if  not len(modified) and not len(deleted) and not len(added):
        console.print("No Changes Were Made",style='bold yellow')
        dirty="Clean"
        console.print(f"Working Tree: {dirty}",style='bold yellow') 
        return
    else:
        if len(added):
            added.insert(0,f'Added Files ({len(added)})')
        
        if len(modified):
            modified.insert(0,f'Modified Files ({len(modified)})')
        
        if len(deleted):
            deleted.insert(0,f'Deleted Files ({len(deleted)})')
        
    for i in added:
        console.print(i,style='bold green')
    if len(added):
        print()
    for i in modified:
        console.print(i,style='bold green')
    if len(modified):
        print()
    for i in deleted:
        console.print(i,style='bold green')
    if len(deleted):
        print()
    console.print(f"Working Tree: {dirty}",style='bold yellow') 