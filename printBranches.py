from json import loads  # noqa: N999
from pathlib import Path

from rich.console import Console

console = Console()
def printBranches():
    with open(Path.cwd()/'.oreon'/'branches.json','r') as f:
        d=loads(f.read())
    with open(Path.cwd()/'.oreon'/'metadata.json','r') as f:
        cur_branch=loads(f.read())['cur_branch']
    for i in d:
        if i==cur_branch:
            console.print('*  ',i,style='bold green')
            continue
        console.print("   ",i,style='bold yellow')