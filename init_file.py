from math import  floor
from typing import *
NUM_INIT_SIZE_BYTES=6
MAX_SIZE=2**(NUM_INIT_SIZE_BYTES*8)
ENCODING="utf-8"
MAXIMUMPATHNUM=2**(8*2)
def encodeInitCompressData(size:int,file:str,codec:dict):
    assert MAX_SIZE>size ,"THE FILE THAT YOU WOULD COMPRESS REACHS THE MAXIMUM SIZE"
    express_size=size.to_bytes(NUM_INIT_SIZE_BYTES,"big")

    yield express_size
    yield InitDir(file)

    yield len(codec).to_bytes(2,"big")
  
  
    for num,binary in codec.items():
        binary=str.encode(binary,ENCODING)
 
        yield int(num).to_bytes(1,"big")+len(binary).to_bytes(1,"big")+binary
 
    
def decodeInitCompressData(data:Iterator[bytes]): 
    size=_getSize(data,NUM_INIT_SIZE_BYTES)
    filePath=InitFileDir(data)
    sizecodecBytes=_getSize(data,2)
    codec=dict()
    for _ in range(sizecodecBytes):
        keyNum=ord(next(data))
        valueNumBytes=ord(next(data)) 
        codekey=b""
        for _ in range(valueNumBytes):
            codekey+=next(data)
        codekey=codekey.decode(ENCODING)
        codec.update({keyNum:codekey})
    return size,filePath,codec


def InitDir(dir:str):
    file_path_bytes=str.encode(dir,ENCODING)
    
    numbytes=len(file_path_bytes)
    assert numbytes<MAXIMUMPATHNUM,"THE FILE REACHED MAXIMUM PATHFILE"
    numbytes=numbytes.to_bytes(2,"big")
    return numbytes+file_path_bytes
def _getSize(data:Iterable[bytes],bytesLenght=2):
    fileLenght=b""
    for _ in range(bytesLenght):
        fileLenght+=next(data)
    return int.from_bytes(fileLenght,"big")
def InitFileDir(data:Iterable[bytes]):
    fileLenght=_getSize(data)
    filePath=b""
    for _ in range(fileLenght):
        filePath+=next(data)
    filePath=filePath.decode("utf-8")
    return filePath
                
def decodeInitDirFile(data:Iterable[bytes]):
    fileLenght=_getSize(data)
    for _ in range(fileLenght):
        yield InitFileDir(data)
    
        
    
    
