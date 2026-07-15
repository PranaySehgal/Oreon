import argparse
from time import sleep
from pathlib import Path
from .__init__ import __init__
from .commit import commitData
from .showCommits import *
from .info import oreanInfo
from .show import oreonShow
from .status import oreanStatus
def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command",required=True)
    init = subparser.add_parser("init")
    commit = subparser.add_parser("commit")
    restore = subparser.add_parser("restore")
    commit.add_argument("-m", "--message", required=False)
    init.add_argument("path",default='.')
    parser.add_argument("--version", action="version", version="Oreon 0.1.0")
    info=subparser.add_parser("info")
    info=subparser.add_parser("status")
    show = subparser.add_parser("show")
    args = parser.parse_args()
    if args.command=='init' and not Path(str(Path.cwd())+parser.parse_args().path).exists():
        print("Sorry, The Path You Mentioned Does Not Exist")
        sleep(2)
        return main()
    elif args.command=='init':
        if Path(str(Path.cwd())+'\\.oreon').exists():
            print("Orean Initialized ::)")
            print("Oreon Has Already Been Initialised In This Directory")
            return
        path = str(Path.cwd())+parser.parse_args().path
        __init__(path=path)
    elif args.command == 'commit':
        if not Path(str(Path.cwd())+'\\.oreon').exists():
            print("Oreon Has Not Been Initialised In This Directory")
            return
        commitData(message= args.message if args.message else None)
    elif args.command=='restore':
        if not Path(str(Path.cwd())+'\\.oreon').exists():
            print("Oreon Has Not Been Initialised In This Directory")
            return
        length,directory = showCommits()
        x=input("Enter the serial number of the commit you want to restore....")
        if not x.isdigit() or int(x)>length or int(x)<1:
            print("Invalid Input")
            return
        else:
            restoreCommit(directory[int(x)-1])
    elif args.command=='info':
        if not Path(str(Path.cwd())+'\\.oreon').exists():
            print("Oreon Has Not Been Initialised In This Directory")
            return
        oreanInfo()
    elif args.command == 'status':
        if not Path(str(Path.cwd())+'\\.oreon').exists():
            print("Oreon Has Not Been Initialised In This Directory")
            return
        oreanStatus()
    elif args.command== 'show':
        if not Path(str(Path.cwd())+'\\.oreon').exists():
            print("Oreon Has Not Been Initialised In This Directory")
            return
        length,directory = showCommits()
        x=input("Enter the serial number of the commit....")
        if not x.isdigit() or int(x)>length or int(x)<1:
            print("Invalid Input")
            return
        else:
            oreonShow(directory,int(x))