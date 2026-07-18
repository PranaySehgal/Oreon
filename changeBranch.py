from pathlib import Path
from json import loads,dumps
from .restore import restoreCommit
from .checkHash import checkHash
def changeExistingBranch(branchName):
    f=open(Path.cwd() / '.oreon' / 'metadata.json','r')
    d=loads(f.read())
    f.close()
    changes=checkHash()[0]
    if changes:
        print("Un-Commited Changes. Aborting!")
        return
    if d['branches'].get(branchName,-90)==-90:
        print("No Such Branch Exists. Select from one of Them",list(d['branches'].keys()))
        return
    if d['cur_branch']==branchName:
        print(f"Already On {branchName}")
        return
    if len(d['branches'][branchName]):
        restoreCommit(d['branches'][branchName][-1])
    f=open(Path.cwd() / '.oreon' / 'metadata.json','w')
    d['cur_branch']=branchName
    f.write(dumps(d))
    f.close()