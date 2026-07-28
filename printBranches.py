from pathlib import Path
from json import loads
from rich.console import Console
console = Console()
def printBranches():
    f=open(Path.cwd()/'.oreon'/'branches.json','r')
    d=loads(f.read())
    f.close()
    f=open(Path.cwd()/'.oreon'/'metadata.json','r')
    cur_branch=loads(f.read())['cur_branch']
    f.close()
    for i in d:
        if i==cur_branch:
            console.print('*  ',i,style='bold green')
            continue
        console.print("   ",i,style='bold yellow')