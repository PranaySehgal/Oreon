from pathlib import Path
from json import loads,dumps
import subprocess
import shutil
from rich.console import Console
console = Console()
def deleteBranch(branchName):
    f = open(Path.cwd()/'.oreon'/'branches.json')
    data = loads(f.read())
    keys = data[branchName]['Hierarchy']
    f.close()
    for i in data:
        if keys in data[i]['Hierarchy'] and i!=branchName:
            console.print("Child Branch Detetced. Removal of leaf branches is allowed ONLY",style='bold red')
            return
    else:
        if data[branchName]=='':
            console.print("Deleting Default Branch Is not Supported",style='bold yellow')
            return
        del data[branchName]
        subprocess.run('oreon changeBranch main')
        shutil.rmtree(Path.cwd()/'.oreon'/'commits'/branchName)
        f = open(Path.cwd()/'.oreon'/'branches.json','w')
        f.write(dumps(data))
        f.close()
        console.print("Branch Deleted Successfully",style='bold green')