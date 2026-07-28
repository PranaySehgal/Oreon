from pathlib import Path
from os import mkdir
from json  import  loads,dumps
import shutil
from .checkHash import checkHash
from getpass import getuser
from datetime import datetime
from rich.console import Console
def createNewBranch(branchName):
    console = Console()
    added,deleted,modified=checkHash()[:-1]
    if added or deleted or modified:
        console.print("Un-Committed Changes, Aborting!",style='bold red')
        return 
    with open(Path.cwd() / '.oreon' / 'branches.json','r') as f:
        d=loads(f.read())
    with open(Path.cwd() / '.oreon' / 'metadata.json','r') as f:
        data = loads(f.read())
    cur_branch=data['cur_branch']
    ignore = data['ignore']
    
    if branchName in d:
        console.print("Branch Already Exists",style='bold red')
        return
    with open(Path.cwd() / '.oreon' / 'branches.json','w') as f:
        d.update({branchName:{}})
        d[branchName]['commits']=[]
        d[branchName]['Hierarchy']=f"{d[cur_branch]['Hierarchy'] if d[cur_branch]['Hierarchy'] else 'main'}+{branchName}"
        d[branchName]['next_commit']=1
        f.write(dumps(d))
    mkdir(Path.cwd() / '.oreon' / 'commits' / branchName)
    mkdir(Path.cwd() / '.oreon' / 'commits' / branchName/'base')
    mkdir(Path.cwd() / '.oreon' / 'commits' / branchName/'base'/'changes')
    with open(Path.cwd() / '.oreon' / 'commits' / branchName / 'base' /'changes'/'metadata.json','w') as f:
        f.write(dumps(
            {
                "Author":getuser(),
                "Date_Created":str(datetime.now()),
                "Message":"Create Branch",
                "Random_Id":"CB1011"
            }
        ))
    array = []
    for i in Path.cwd().rglob("*"):
        if i.is_file() and '.oreon' not in str(i):
            array.append(str(i.relative_to(Path.cwd())))
    with open(Path.cwd() / '.oreon' / 'commits' / branchName / 'base' /'changes'/'changes.json','w')as f:
        f.write(dumps(
            {
                "updated":[],
                "deleted":[],
                "added":array,
            }
        ))
    
    shutil.copytree(Path.cwd(),Path.cwd() / '.oreon' / 'commits' / branchName/'base'/'changes'/'src',ignore=shutil.ignore_patterns(".oreon",*ignore))
    console.print("Branch Created Successfully",style='bold green')