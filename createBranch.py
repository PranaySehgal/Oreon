from pathlib import Path
from os import mkdir
from json  import  loads,dumps
def createNewBranch(branchName):
    f=open(Path.cwd() / '.oreon' / 'metadata.json','r')
    d=loads(f.read())
    f.close()
    if d['branches'].get(branchName,-90)!=-90:
        print("Branch Already Exists!")
        return
    f=open(Path.cwd() / '.oreon' / 'metadata.json','w')
    d['branches'][branchName]=[]
    
    f.write(dumps(d))
    f.close()
    mkdir(Path.cwd() / '.oreon' / 'commits' / branchName)
    