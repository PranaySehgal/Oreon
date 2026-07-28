from rich.console import Console
from pathlib import Path
from json import loads
console = Console()
def ignore():
    with open(Path.cwd()/'.oreon'/'metadata.json') as file:
        d=loads(file.read())
        ignore = d['ignore']
        with open(Path.cwd()/'.oreonignore','w') as ignoreFile:
            ignoreFile.writelines(ignore)
    console.print('.oreonignore has been revealed in your directory for further edition and will be hidden on your next commit')
