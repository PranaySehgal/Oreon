from pathlib import Path
from json import loads
def printBranches():
    f=open(Path.cwd()/'.oreon'/'metadata.json','r')
    d=loads(f.read())
    for i in d['branches']:
        if i==d['cur_branch']:
            print('*  ',i)
            continue
        print("   ",i)