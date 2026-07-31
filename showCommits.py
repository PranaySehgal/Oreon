from json import loads  # noqa: N999
from pathlib import Path

import tabulate
from rich.console import Console

from .show import oreonShow

console = Console()
def showCommits(action):
    path = str(Path.cwd())
    with open(Path.cwd()/'.oreon'/'branches.json','r') as f:
          d = loads(f.read())
    with open(Path.cwd()/'.oreon'/'metadata.json','r') as f:
          cur_branch = loads(f.read())['cur_branch']
    metadata=[['Serial Number','Message','Date Created','Branch','Author']]
    ids = []
    
    l = Path(f"{path}/.oreon/commits/{cur_branch}").iterdir()
    for j in l:
        if j.is_dir():
            with open(f"{j}\\changes\\metadata.json") as file:
               d=file.read()
        else:
            continue
        data = loads(d)
        file.close()
        ids.append(data['Random_Id'])
        metadata.append([data['Random_Id'],data['Message']  if data['Message'] else "No Commit Message",data['Date_Created'],cur_branch,data['Author']])
    console.print(tabulate.tabulate(metadata,tablefmt="fancy_grid"),style='bold green')
    if action=='show':
       x=input("Enter the serial number of the commit you want to view....")
       for i in ids:
           if x==i:
               break
       else:
            console.print("Invalid Input",style='bold red')
            return
        
       if x=='CB1011':
            oreonShow(cur_branch,'base')
       else:
            x=ids.index(x)
            oreonShow(metadata[int(x+1)][-2],int(x+1))
    elif action=='restore':
       x=input("Enter the serial number of the commit you want to restore....")
       for i in ids:
            if x==i:
                break
       else:
            console.print("Invalid Input",style='bold red')
            return
       if x=='CB1011':
            return x
       else:
           
            x=ids.index(x)
            return x+1