from math import  floor
from typing import *
NUM_INIT_SIZE_BYTES=6
MAX_SIZE=2**(NUM_INIT_SIZE_BYTES*8)
ENCODING="utf-8"
MAXIMUMPATHNUM=32000
MAXDICTSIZE=3
def encodeInitCompressData(file:str,size:int,codec:dict):
    assert MAX_SIZE>size ,"THE FILE THAT YOU WOULD COMPRESS REACHS THE MAXIMUM SIZE"
    express_size=size.to_bytes(NUM_INIT_SIZE_BYTES,"big")
    yield express_size
    
    file_path_bytes=str.encode(file,ENCODING)
    numbytes=len(file_path_bytes)
    assert numbytes<MAXIMUMPATHNUM,"THE FILE REACHED MAXIMUM PATHFILE"
    numbytes=numbytes.to_bytes(2,"big")
    yield numbytes+file_path_bytes
    
    bytesencodings=map(lambda x:str.encode(x,ENCODING),codec.values())
    
    dictNumBytes=sum(map(lambda x:len(x)+2,bytesencodings))
    yield dictNumBytes.to_bytes(MAXDICTSIZE,"big")
  
 
    for num,binary in codec.items():
        binary=str.encode(binary,ENCODING)
        yield int(num).to_bytes(1,"big")+len(binary).to_bytes(1,"big")+binary
    
    
def decodeInitCompressData(data:Iterator[bytes]): 
    size=b""
    for _ in range(NUM_INIT_SIZE_BYTES):
        size+=next(data)
    fileLenght=b""
    for _ in range(2):
        fileLenght+=next(data)
    filePath=b""
    for _ in range(int.from_bytes(fileLenght,"big")):
        filePath+=next(data)
    filePath=filePath.decode("utf-8")
   
    sizecodecBytes=b""
    for _ in range(MAXDICTSIZE):
        sizecodecBytes+=next(data)  
    sizecodecBytes=int.from_bytes(sizecodecBytes,"big")
    
    n=0
    codec=dict()
    while n<sizecodecBytes:
        
        keyNum=ord(next(data))
        valueNumBytes=ord(next(data)) 
        codekey=b""
        for _ in range(valueNumBytes):
            codekey+=next(data)
        codekey=codekey.decode(ENCODING)
        codec.update({keyNum:codekey})
        n+=2+valueNumBytes
    
    return filePath,int.from_bytes(size,"big"),codec

def __test():
    org_size=12*(1024**2)
    data=encodeInitCompressData("file.py",org_size,{1:"010010",2:"01",5:"012012"})
    result=b""
    for x in data:
        result+=x
    
    L = (result[i:i+1] for i in range(len(result)))
    result_decodint =decodeInitCompressData(L)
    print(result_decodint)
    
if __name__=="__main__":
    __test()