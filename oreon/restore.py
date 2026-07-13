from pathlib import Path
from json import loads
import shutil,os
def restoreCommit(x):
    files = sorted(
    Path(str(Path.cwd())+'//.oreon//commits//').iterdir(),
    key=lambda p: p.stat().st_mtime,
    reverse=True)
    for i in range(len(files)):
        files[i]=files[i].absolute()
    index=files.index(Path(str(Path.cwd())+'\\.oreon\\commits\\'+x))
    files=files[:index+1]
    for k in Path.cwd().iterdir():
            if k.name=='.oreon':
                continue
            elif k.is_dir():
                shutil.rmtree(k)
            else:
                k.unlink()
    shutil.copytree(str(Path.cwd())+'\\.oreon\\latest\\',str(Path.cwd()),dirs_exist_ok=True)
    for i in files:
        changes=loads(open(str(i)+'\\changes\\changes.json').read())
        for j in changes:
            if changes[j][1]=="updated" or changes[j][1]=="deleted":
                destination = Path.cwd() / changes[j][0]
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(str(i)+'\\changes\\src\\'+changes[j][0],destination)
            else:
                if Path(str(Path.cwd())+"\\"+changes[j][0]).exists():
                    os.remove(str(Path.cwd())+"\\"+changes[j][0])
    