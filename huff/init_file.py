from math import  floor
from typing import *
from __funct import *
def encodeInitCompressData(size:int,file:str,codec:dict):
    yield encodeInit(size,file)
    yield len(codec).to_bytes(1,"big")
    for num,binary in codec.items():
        binary=str.encode(binary,ENCODING)
        yield int(num).to_bytes(1,"big")+len(binary).to_bytes(1,"big")+binary

    
def decodeInitCompressData(data:Iterator[bytes]): 
    size,filePath=decodeInit(data)
    sizecodecBytes=getSize(data,1)
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




                

    
        
    
    
