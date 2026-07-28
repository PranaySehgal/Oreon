from json import loads
from pathlib import Path
import tabulate
from .show import oreonShow
from rich.console import Console
console = Console()
def showCommits(action):
    path = str(Path.cwd())
    f=open(Path.cwd()/'.oreon'/'branches.json','r')
    d = loads(f.read())
    f.close()
    f=open(Path.cwd()/'.oreon'/'metadata.json','r')
    cur_branch = loads(f.read())['cur_branch']
    f.close()
    metadata=[['Serial Number','Message','Date Created','Branch','Author']]
    ids = []
    
    l = Path(f"{path}/.oreon/commits/{cur_branch}").iterdir()
    for j in l:
        if j.is_dir():
            file=open(f"{j}\\changes\\metadata.json")
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