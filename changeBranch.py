from json import dumps, loads  # noqa: N999
from pathlib import Path

from rich.console import Console

from .checkHash import checkHash
from .restore import restoreCommit


def changeExistingBranch(branchName):
    console = Console()
    with open(Path.cwd() / '.oreon' / 'branches.json','r') as f:
        d=loads(f.read())
    with open(Path.cwd() / '.oreon' / 'metadata.json','r') as f:
        metadata=loads(f.read())
        cur_branch=metadata['cur_branch']
    updated,added,deleted,_data=checkHash()
    if added or updated or deleted:
        console.print("Un-Committed Changes. Aborting!",style='bold red')
        return
    if branchName not in d:
        console.print("No Such Branch Exists. Select from one of Them",list(d.keys()),style='bold yellow')
        return
    if cur_branch==branchName:
        console.print(f"Already On {branchName}",style='bold cyan')
        return
    if len(d[branchName]['commits']):
        restoreCommit(d[branchName]['commits'][-1],branch=branchName)
    else:
        restoreCommit(1,branch=branchName)
    with open(Path.cwd() / '.oreon' / 'metadata.json','w') as f:
        metadata['cur_branch']=branchName
        f.write(dumps(metadata))
    console.print(f"Branch Changed from {cur_branch}->{branchName}",style='bold green')