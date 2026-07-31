import hashlib  # noqa: N999
from json import dumps, loads
from pathlib import Path


def checkHash():
    files=[]
    pathFiles = Path.cwd().rglob("*")
    with open(Path.cwd()/'.oreon'/'metadata.json') as f:
        metadata = loads(f.read())
        ignore = metadata['ignore']
    for i in pathFiles:
        source=Path(i)
        if '.oreon' in str(i) or '.git' in str(i):
            continue
        elif i.is_file() and '.oreon' not in str(i) and '.git' not in str(i):
            files.append(str(source))
    data = {}
    with open(Path.cwd()/".oreon"/"hashes.json",'r') as f:
        prev_data = loads(f.read())
    for i in files:
        with open(Path.cwd()/i,'rb') as temp:
            contents = temp.read()
        source = Path(i).relative_to(Path.cwd())
        ignoreFiles = False
        pattern = False
        for j in ignore:
            if str(j) == str(source):
                ignoreFiles=True
                break
            elif Path(Path.cwd()/j).is_dir():
                if str(Path(Path.cwd()/j)) in str(Path(Path.cwd()/i).parent) and i and j:
                    ignoreFiles=True
                    pattern=True
                    break
            elif '*.' in j:
                fileData = j.split("*")
                file_extension = fileData[1]
                file_path = fileData[0]
                if  Path(Path.cwd()/file_path)== Path(Path.cwd()/source.parent) and  file_extension==str(source.suffix):
                    ignoreFiles=True
                    pattern=True
                    break
        if ignoreFiles and str(source) not in prev_data:
            continue
        elif ignoreFiles and Path(i).is_file() and not pattern:
            ignore.remove(str(source))
        hash = hashlib.sha256(contents)
        data[str(source)]=str(hash.hexdigest())
    updated=[]
    deleted=[]
    added=[]
    with open(Path.cwd()/'.oreon'/'metadata.json','w') as f:
        metadata['ignore']=ignore
        f.write(dumps(metadata))
    
    for i in prev_data:
        if data.get(i,-90)!=-90 and prev_data[i]!=data[i]:
            updated.append(str(i))
        elif prev_data.get(i,-90)!=-90 and data.get(i,-90)==-90:
            if i in ignore:
                continue       
            else:
                deleted.append(str(i))
    for i in data:
        if prev_data.get(i,-90)==-90:
            added.append(str(i))
    # with open(Path.cwd()/'.oreon'/'hashes.json','w') as f:
    #     f.write(dumps(data))
    return updated,added,deleted,data