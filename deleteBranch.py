import shutil  # noqa: N999
import subprocess
from json import dumps, loads
from pathlib import Path

from rich.console import Console

console = Console()
def deleteBranch(branchName):
    with open(Path.cwd()/'.oreon'/'branches.json') as f:
        data = loads(f.read())
    keys = data[branchName]['Hierarchy']
    for i in data:
        if keys in data[i]['Hierarchy'] and i!=branchName:
            console.print("Child Branch Detected. Removal of leaf branches is allowed ONLY",style='bold red')
            return
    
    if data[branchName]=='':
        console.print("Deleting Default Branch Is not Supported",style='bold yellow')
        return
    del data[branchName]
    subprocess.run('oreon changeBranch main',check=False)
    shutil.rmtree(Path.cwd()/'.oreon'/'commits'/branchName)
    with open(Path.cwd()/'.oreon'/'branches.json','w') as f:
        f.write(dumps(data))
    console.print("Branch Deleted Successfully",style='bold green')