This is how this application works in this version 2.0.0

Oreon is divided into various pieces which are woven into perfection into by cli.py which is the entry point for this oreon. cli embeds all the functionalities into the command prompt panel and provides necessary arguments so that each function can do the mandatory tasks freely. 

changeBranch.py changes the current branch by editing metadata.py which stores all the important information regarding the program like the current working branch, version and date the program was initialized.

checkHash.py matches the current working directory files with previous versions and checks if their hashes have changed, a way of knowing which files have been added , deleted and modified

commit.py commits the the current change to the directory. it stores which files have changed, added or removed, only copy of these which have been added, changed or removed. It maintains metadata file which stores who, when and in which branch created the commit and message given at the time of making a commit.

createBranch.py creates an entry of given branchName in branches.json file  and creates a folder with that name with mandatory information

deleteBranch.py deletes the branch from branches.json file and deletes the folders if the branch is a leaf branch. Child branches can't be removed until their leaf branches are deleted. 

Info.py gives information about current repository

merge.py merges the two given commits by creating the latest snapshots of the two branches and comparing them. If any mergeConflict happens the instructions are given to resolve them

printBranches prints all the branches ever initialized in the repository and marks the current branch.

renameBranch changes branches.json file and the folder that stores all the commits in the file

restore.py restores undoes all the changes and restores to current state.

show.py shows which all changes were done in which commit

showCommits.py shows the commit names, branch name, owner name, date_created and message given, in the command shell in a tabular format. Then the  user can easily enter the random uuid of the commit and access the commit changes

status.py shows if the current repo is clean or dirty.

