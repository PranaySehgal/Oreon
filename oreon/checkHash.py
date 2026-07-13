import os,hashlib,json
from pathlib import Path
files = []
dirs=[]
def fetchFiles(path):
    l = os.listdir(path)
    path+='\\'
    for i in l: 
        if Path(path+i).suffix:
            files.append(path+i) 
        else:
            fetchFiles(path+i)
    
def checkHash():
    path = str(Path.cwd())
    l = os.listdir(path)
    path+='\\'
    for i in l: 
        if i=='.oreon':
            continue
        if Path(path+i).suffix:
            files.append((path+i)) 
        else:
            dirs.append(path+i)
    for i in dirs:
        fetchFiles(i)
    
    data = {}
    f=open(path+"\\.oreon\\hashes.json",'r')
    for i in files:
        temp = open(i,'r').read()
        hash = hashlib.sha256(bytes(temp.encode()))
        data[str(Path(i).relative_to(Path.cwd()))]=str(hash.hexdigest())
    prev_data = json.loads(f.read())
    changes={}
    for i in prev_data:
        if data.get(i,-90)!=-90 and prev_data[i]!=data[i]:
            changes[i]=[i,'updated']
        elif prev_data.get(i,-90)!=-90 and data.get(i,-90)==-90:
            changes[i]=[i,'deleted']
    for i in data:
        if prev_data.get(i,-90)==-90:
            changes[i]=[i,'added']
    return changes,data