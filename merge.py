import shutil
import os
from .checkHash import checkHash
from subprocess import run
from pathlib import Path
from json import loads
from uuid import uuid1
from rich.console import Console
console = Console()
def restoreChanges(branchName):
    folder = Path(Path.cwd()/'.oreon'/'commits'/branchName).iterdir()
    shutil.copytree(Path.cwd()/'.oreon'/'commits'/branchName/'base'/'changes'/'src',Path.cwd()/'.oreon'/'commits'/branchName/'temp',ignore=shutil.ignore_patterns("metadata.json"))
    for i in folder:
        if i.name=='base':
            continue
        elif i.is_dir():
            with open(i/'changes'/'changes.json') as f:
                d=loads(f.read())   
            modified=d['updated']
            deleted=d['deleted']
            added=d['added']
            f.close()
            for j in modified:
                os.remove(Path.cwd()/'.oreon'/'commits'/branchName/'temp'/j)
                if not Path(Path.cwd()/'.oreon'/'commits'/branchName/'temp'/j).exists():
                    Path(Path.cwd()/'.oreon'/'commits'/branchName/'temp'/j).parent.mkdir(parents=True,exist_ok=True)
                shutil.copy(i/'changes'/'src'/j,Path.cwd()/'.oreon'/'commits'/branchName/'temp'/j)
            for j in deleted:
                if Path(Path.cwd()/'.oreon'/'commits'/branchName/'temp'/j).exists():
                    os.remove(Path.cwd()/'.oreon'/'commits'/branchName/'temp'/j)
            for j in added:
                if not Path(Path.cwd()/'.oreon'/'commits'/branchName/'temp'/j).exists():
                    Path(Path.cwd()/'.oreon'/'commits'/branchName/'temp'/j).parent.mkdir(parents=True,exist_ok=True)
                shutil.copy(i/'changes'/'src'/j,Path.cwd()/'.oreon'/'commits'/branchName/'temp'/j)
def mergeBranches(parent, branchName):
    added,deleted,modified=checkHash()[:3]
    if added or deleted or modified:
        console.print("Un-committed Changed, Aborting Immediately!",style='bold red')
        return
    
    with open(Path.cwd()/'.oreon'/'branches.json') as f:
        d = loads(f.read())
    branches=d[branchName]['Hierarchy'].split("+")

    if d[parent]==d[branchName]:
        console.print("Invalid Input",style='bold red')
        return
    l1 = d[branchName]['Hierarchy'].split("+")
    l2 = d[parent]['Hierarchy'].split("+")
    if len(l1) and len(l2) and l1[:-1]==l2[:-1] and l1[-1]!=l2[-1]:
        branches=[parent,branchName]
    else:
        x = branches.index(parent)
        branches = branches[x:]
    to_be_merged_with = branches[0]
    run(f"oreon changeBranch {to_be_merged_with}",check=False)
    randomName = str(uuid1())
    for i in range(1,len(branches)):
        restoreChanges(branches[i])
        src = Path.cwd()/'.oreon'/'commits'/branchName/'temp'
        for j in Path(src).rglob("*"):
            if j.is_file():
                source = j.relative_to(src)
                dest= Path.cwd()/source
                if not  Path(dest).exists():
                    Path(dest).parent.mkdir(parents=True,exist_ok=True)
                    shutil.copy(j,dest)
                elif Path(dest).exists():
                    with open(j) as f:
                        data1 = f.read()
                    with open(dest) as f:
                        data2 = f.read()
                    if data1!=data2:
                        os.mkdir(Path.cwd()/randomName)
                        os.mkdir(Path.cwd()/randomName/'1')
                        os.mkdir(Path.cwd()/randomName/'2')
                        shutil.copy(j,Path.cwd()/randomName/'1')
                        shutil.copy(dest,Path.cwd()/randomName/'2')
                        input(f"Conflict Occurred, There is a  folder in the base directory with this name{randomName}. After deciding which one to keep, kindly delete the other one and type anything and press enter. Its a temporary copy only.")
                        files=[]
                        for k in Path(Path.cwd()/randomName).rglob("*"):
                            if k.is_file():
                                files.append(k)
                        os.remove(dest)
                        if len(files)!=1:
                            console.print("As you have not made a decision, we are restoring the previous data and overriding current one",style='bold yellow')
                            shutil.copy(j,Path.cwd())
                        else:
                            shutil.copy(files[0],dest)
                        shutil.rmtree(Path.cwd()/randomName)
        shutil.rmtree(Path.cwd()/'.oreon'/'commits'/branches[i]/'temp')
        run(f"oreon commit -m 'Merged_With_{branches[i]}'",check=False)
        run(f"oreon changeBranch {branches[i]}",check=False)
        run("oreon commit -m 'CB1011MERGECOMMIT'",check=False)
        run(f"oreon changeBranch {to_be_merged_with}",check=False)
        console.print("Branches Merged Successfully",style='bold green')