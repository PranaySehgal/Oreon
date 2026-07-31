import os  # noqa: N999
from json import dumps, loads
from pathlib import Path

from rich.console import Console

console = Console()
def renameBranch(original,final):
    with open(Path.cwd()/'.oreon'/'branches.json') as file:
        d = loads(file.read())
    x=d[original]
    del d[original]
    d[final]=x
    hierarchy = d[final]['Hierarchy']
    for i in d:
        if hierarchy in d[i]['Hierarchy']:
            indexOfOriginal=d[i]['Hierarchy'].split("+").index(original)
            new='+'.join(d[i]['Hierarchy'].split("+")[:indexOfOriginal])+'+'+final
            new+=('+'+'+'.join(d[i]['Hierarchy'].split("+")[indexOfOriginal+1:])) if len(d[i]['Hierarchy'].split("+")[indexOfOriginal+1:]) else ''
            d[i]['Hierarchy']=new
    with open(Path.cwd()/'.oreon'/'branches.json','w') as file:
        file.write(dumps(d))
    with open(Path.cwd()/'.oreon'/'metadata.json','r') as file:
        data = loads(file.read())
    data['cur_branch']=final
    with open(Path.cwd()/'.oreon'/'metadata.json','w') as file:
        file.write(dumps(data))
    os.rename(Path.cwd()/'.oreon'/'commits'/original, Path.cwd()/'.oreon'/'commits'/final)
    console.print(f"Action Completed: Rename Branch({original}->{final})",style='bold green')
    