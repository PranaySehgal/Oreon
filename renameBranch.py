from pathlib import Path
from json import loads,dumps
import os
from rich.console import Console
console = Console()
def renameBranch(original,final):
    file = open(Path.cwd()/'.oreon'/'branches.json')
    d = loads(file.read())
    file.close()
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
    file = open(Path.cwd()/'.oreon'/'branches.json','w')
    file.write(dumps(d))
    file.close()
    file = open(Path.cwd()/'.oreon'/'metadata.json','r')
    data = loads(file.read())
    file.close()
    data['cur_branch']=final
    file = open(Path.cwd()/'.oreon'/'metadata.json','w')
    file.write(dumps(data))
    file.close()
    os.rename(Path.cwd()/'.oreon'/'commits'/original, Path.cwd()/'.oreon'/'commits'/final)
    console.print(f"Action Completed: Rename Branch({original}->{final})",style='bold green')
    