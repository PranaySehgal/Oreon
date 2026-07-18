import argparse
from time import sleep
from pathlib import Path
from .__init__ import __init__
from .commit import commitData
from .changeBranch import changeExistingBranch
from .showCommits import *
from .info import oreanInfo
from .show import oreonShow
from .createBranch import createNewBranch
from .status import oreanStatus
def checkExistence():
        if not Path(str(Path.cwd())+'\\.oreon').exists():
            print("Oreon Has Not Been Initialised In This Directory")
            return False
        return True
def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command",required=True)
    init = subparser.add_parser("init")
    commit = subparser.add_parser("commit")
    subparser.add_parser("restore")
    commit.add_argument("-m", "--message", required=False)
    changeBranch = subparser.add_parser("changeBranch")
    changeBranch.add_argument("branch_name")
    createBranch = subparser.add_parser("createBranch")
    createBranch.add_argument("branch_name")
    init.add_argument("path",default='.')
    parser.add_argument("--version", action="version", version="Oreon 0.1.0")
    subparser.add_parser("info")
    subparser.add_parser("status")
    subparser.add_parser("show")
    args = parser.parse_args()
    if args.command=='init' and not Path(str(Path.cwd())+parser.parse_args().path).exists():
        print("Sorry, The Path You Mentioned Does Not Exist")
        sleep(2)
        return main()
    elif args.command=='init':
        if Path(str(Path.cwd())+'\\.oreon').exists():
            print("Oreon Has Already Been Initialised In This Directory")
            return
        path = str(Path.cwd())+parser.parse_args().path
        __init__(path=path)
    elif args.command == 'commit':
        if not checkExistence():
            return
        commitData(message= args.message if args.message else None)
    elif args.command=='restore':
        if not checkExistence():
            return
        length=showCommits()
        x=input("Enter the serial number of the commit you want to restore....")
        if not x.isdigit() or int(x)>length or int(x)<1:
            print("Invalid Input")
            return
        else:
            restoreCommit(x)
    elif args.command=='info':
        if not checkExistence():
            return
        oreanInfo()
    elif args.command == 'status':
        if not checkExistence():
            return
        oreanStatus()
    elif args.command== 'show':
        if not checkExistence():
            return
        length=showCommits()
        x=input("Enter the serial number of the commit you want to view....")
        if not x.isdigit() or int(x)>length or int(x)<1:
            print("Invalid Input")
            return
        else:
            oreonShow(x)
    elif args.command=='changeBranch':
        if not checkExistence():
            return
        changeExistingBranch(args.branch_name)
        pass
    
    elif args.command=='createBranch':
        if not checkExistence():
            return
        createNewBranch(args.branch_name)
        pass
    