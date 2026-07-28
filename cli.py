import argparse
from pathlib import Path

from .__init__ import __init__
from .changeBranch import changeExistingBranch
from .commit import commitData
from .createBranch import createNewBranch
from .deleteBranch import deleteBranch
from .ignore import ignore
from .info import oreanInfo
from .merge import mergeBranches
from .printBranches import printBranches
from .renameBranch import *
from .restore import restoreCommit
from .showCommits import *
from .status import oreanStatus


def checkExistence():
        if not Path(str(Path.cwd())+'\\.oreon').exists():
            console.print("Oreon Has Not Been initialized In This Directory",style='bold yellow')
            return False
        return True
def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command",required=True)
    subparser.add_parser("init")
    commit = subparser.add_parser("commit")
    restore=subparser.add_parser("restore")
    restore.add_argument("--preview",action='store_true',help="Preview changes without applying them.")
    commit.add_argument("-m", "--message", required=False)
    changeBranch = subparser.add_parser("changeBranch")
    changeBranch.add_argument("branch_name")
    createBranch = subparser.add_parser("createBranch")
    createBranch.add_argument("branch_name")
    parser.add_argument("--version", action="version", version="Oreon 1.2.0")
    renameBranchOreon = subparser.add_parser("renameBranch")
    renameBranchOreon.add_argument("branch1")
    renameBranchOreon.add_argument("branch2")
    subparser.add_parser("info")
    subparser.add_parser("branches")
    subparser.add_parser("status")
    subparser.add_parser("show")
    merge = subparser.add_parser("merge")
    merge.add_argument("parent")
    merge.add_argument("child")
    delete = subparser.add_parser("delete")
    delete.add_argument("branchName")
    subparser.add_parser("editIgnore")
    args = parser.parse_args()
    
    if args.command=='init':
        if Path(str(Path.cwd())+'\\.oreon').exists():
            console.print("Oreon Has Already Been Initialized In This Directory",style='bold yellow')
            return
        path = str(Path.cwd())
        __init__(path=path)
    elif args.command == 'commit':
        if not checkExistence():
            return
        commitData(message= args.message if args.message else None)
    elif args.command=='restore':
        if not checkExistence():
            return
        x=showCommits('restore')
        restoreCommit(x,args.preview)
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
        showCommits('show')
    elif args.command=='changeBranch':
        if not checkExistence():
            return
        changeExistingBranch(args.branch_name)
        
    
    elif args.command=='createBranch':
        if not checkExistence():
            return
        createNewBranch(args.branch_name)
        
    elif args.command=='branches':
        printBranches()
    elif args.command=='branches':
        if not checkExistence():
            return
        printBranches()
    
    elif args.command=='renameBranch':
        if not checkExistence():
            return
        renameBranch(args.branch1,args.branch2)
    
    elif args.command=='merge':
        if not checkExistence():
            return
        mergeBranches(args.parent,args.child)
    elif args.command=='delete':
        if not checkExistence():
            return
        deleteBranch(args.branchName)
    elif args.command=='editIgnore':
        ignore()