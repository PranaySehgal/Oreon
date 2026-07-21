from pathlib import Path
from json import loads,dumps
import os
def renameBranch(original,final):
    file = open(Path.cwd()/'.oreon'/'metadata.json')
    d = loads(file.read())
    file.close()
    x=d['branches'][original]
    del d['branches'][original]
    d['branches'][final]=x
    d['cur_branch']=final
    file = open(Path.cwd()/'.oreon'/'metadata.json','w')
    file.write(dumps(d))
    file.close()
    print(help(os.rename))
    os.rename(Path.cwd()/'.oreon'/'commits'/original, Path.cwd()/'.oreon'/'commits'/final)
    print(f"Action Completed: Rename Branch({original}->{final})")