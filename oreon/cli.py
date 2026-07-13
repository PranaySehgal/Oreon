import argparse
from time import sleep
from pathlib import Path
from .__init__ import __init__
from .commit import commitData
from .showCommits import *
def main():
    print("Orean Initialized ::)")
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command",required=True)
    init = subparser.add_parser("init")
    commit = subparser.add_parser("commit")
    restore = subparser.add_parser("restore")
    commit.add_argument("-m", "--message", required=False)
    init.add_argument("path",default='.')
    args = parser.parse_args()
    if args.command=='init' and not Path.exists(str(Path.cwd())+parser.parse_args().path):
        print("Sorry, The Path You Mentioned Does Not Exist")
        sleep(2)
        return main()
    elif args.command=='init':
        path = str(Path.cwd())+parser.parse_args().path
        __init__(path=path)
    elif args.command == 'commit':
        commitData(message= args.message if args.message else None)
    elif args.command=='restore':
        showCommits()