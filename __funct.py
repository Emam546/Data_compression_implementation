from typing import Iterable
from pycv2.tools.utils import createProgressBar,progressBar
import os,inspect
from typing import *
MAXIMUMPATHNUM=2**(8*2)
ENCODING="utf-8"
NUM_INIT_SIZE_BYTES=6
MAX_SIZE=2**(NUM_INIT_SIZE_BYTES*8)
def getDataBytes(file,tickEvery=0.2)->bytes:
    complete_size=os.stat(file).st_size
    tickEvery=round((tickEvery*complete_size)/100)
    progressBar=createProgressBar(total=complete_size)
    with open(file,"rb") as f:
        for curr in range(complete_size):
            if (curr%tickEvery)==0:
                progressBar(curr)
            yield f.read(1)
    progressBar(complete_size)
    print()
def getData(file)->int:
    for byte in getDataBytes(file):
        yield ord(byte)

def lastPath(funct):
    LastPath=os.path.abspath(os.curdir)
    if inspect.isgeneratorfunction(funct):
        def adder(*args,**kwargs):
            for data in funct(*args,**kwargs):
                yield data
            os.chdir(LastPath)
    else:
        def adder(*args,**kwargs):
            res=funct(*args,**kwargs)
            os.chdir(LastPath)
            return res
    return adder


@lastPath 
def getALLFiles(dirFile,root=True):
    if root:
        os.chdir(os.path.dirname(dirFile))
        dirFile=os.path.basename(dirFile)
    if not os.path.isdir(dirFile):
        yield dirFile
        raise StopIteration
    
    for child in os.listdir(dirFile):
        childPath=os.path.join(dirFile,child)
        if os.path.isdir(childPath):
            for minchild in getALLFiles(childPath,False):
                yield minchild
        elif os.path.isfile(childPath):
            yield childPath
        else:
            raise "THE PATH IS NOT COMPRESSABLE"
@lastPath
def getAlldirs(dirFile,root=True):
    if root:
        os.chdir(os.path.dirname(dirFile))
        dirFile=os.path.basename(dirFile)
    if not os.path.isdir(dirFile): 
        raise StopIteration
    
    for child in os.listdir(dirFile):
        childPath=os.path.join(dirFile,child)
        if os.path.isdir(childPath):
            for minchild in getAlldirs(childPath,False):
                yield minchild  
def encodeInit(size:int,file:str):
    assert MAX_SIZE>size ,"THE FILE THAT YOU WOULD COMPRESS REACHS THE MAXIMUM SIZE"
    express_size=size.to_bytes(NUM_INIT_SIZE_BYTES,"big")
    return express_size+InitDir(file)
def getSize(data:Iterable[bytes],bytesLenght=2):
    fileLenght=b""
    for _ in range(bytesLenght):
        fileLenght+=next(data)
    return int.from_bytes(fileLenght,"big")
def decodeInit(data:Iterator[bytes]):
    size=getSize(data,NUM_INIT_SIZE_BYTES)
    filePath=InitFileDir(data)
    return size,filePath
def InitFileDir(data:Iterable[bytes]):
    fileLenght=getSize(data)
    filePath=b""
    for _ in range(fileLenght):
        filePath+=next(data)
    filePath=filePath.decode(ENCODING)
    return filePath
def decodeInitDirFile(data:Iterable[bytes]):
    fileLenght=getSize(data)
    for _ in range(fileLenght):
        yield InitFileDir(data)

def InitDir(dir:str):
    file_path_bytes=str.encode(dir,ENCODING)
    
    numbytes=len(file_path_bytes)
    assert numbytes<MAXIMUMPATHNUM,"THE FILE REACHED MAXIMUM PATHFILE"
    numbytes=numbytes.to_bytes(2,"big")
    return numbytes+file_path_bytes
def WriteAllDirs(files:Iterable[str]):
        n=0
        AllDirs=b""
        for dirFile in files:
            for dir in getAlldirs(dirFile):
                AllDirs+=InitDir(dir)
                n+=1
        return n.to_bytes(2,"big")+AllDirs
        
    
