from math import log2
import os
from typing import *
from __funct import *
import io

def transferData(data:Iterable[bytes],presentByte=2,storedDict=None):
    if not storedDict:print("COMPRESSING THE FILE")
    storedDict={b"":0}
    currentByte=b""
    for byte in data:
        if currentByte in storedDict:
            currentIndex=storedDict[currentByte]
            currentByte+=byte
            continue
        yield currentIndex.to_bytes(presentByte,"big")
        storedDict.update({ currentByte:len(storedDict)})
        yield currentByte[-1:]
        currentByte=byte
        currentIndex=0
    if currentByte:
        if currentByte in storedDict:
            currentIndex=storedDict[currentByte]
            yield currentIndex.to_bytes(presentByte,"big")
        elif len(currentByte)==1:
            yield (0).to_bytes(presentByte,"big")
            yield currentByte[-1:]
        else:
            data=(currentByte[x:x+1] for x in range(len(currentByte)))
            for x in transferData(data,storedDict,True):
                yield x



    #print(list(map(lambda x:x,storedDict.keys())))
def retransferData(data:Iterable[bytes],presentByte=3):
    storedDict=[b""]
    
    while True:
        try:
            num=b""
            for _ in range(presentByte):
                num+=next(data)
            index=int.from_bytes(num,"big")
            yield storedDict[index]
            newByte=next(data)
            returnedData=storedDict[index]+newByte
            storedDict.append(returnedData)
            yield newByte
            
        except StopIteration:
            break


def transferDataFile(files:Iterable[bytes],resultfile:str):
    files=files if isinstance(files,list) else [files]  
    assert( not resultfile in files) \
        ,"the orginal file and resultfile must be no same"
    org_size=0
    with open(resultfile,"wb") as resultf:
        resultf.write(WriteAllDirs(files))  
        for dirFile in files:
            cursor_now=resultf.tell()
            filesdir=getALLFiles(dirFile)
            filesCompletePath=getALLFiles(dirFile,False)
            for file,fileName in zip(filesCompletePath,filesdir):
                size=os.stat(file).st_size
                org_size+=size
                presentnum=round(log2(size)/7)
                print(f"THE PRESENTING NUM OF BYTES IS EQUAL To {presentnum}")
                sizeofbytes=0
                addedBytes=0
                InitCode=encodeInit(0,fileName)
                resultf.write(InitCode)
                addedBytes+=len(InitCode)
                for byte in transferData(getDataBytes(file),presentnum):
                    resultf.write(byte)
                    sizeofbytes+=len(byte)
                addedBytes+=sizeofbytes
                resultf.seek(cursor_now)
                resultf.write(sizeofbytes.to_bytes(NUM_INIT_SIZE_BYTES,"big"))
                resultf.seek(0,io.SEEK_END)
    result_size=os.stat(resultfile).st_size
    print(f"the File redced by {round(100-(result_size/org_size)*100,2)}%")
@lastPath
def retransferDataFile(file,resultPath="."):
    print("DECOMPRESSING FILE")
    data=getDataBytes(os.path.abspath(file))
    os.chdir(resultPath)
    for dir in decodeInitDirFile(data):
        if not os.path.exists(dir):
            os.makedirs(dir)
    while True:
        try:
            dataSize,fileName=decodeInit(data)
            presentNum=int.from_bytes(next(data))
            print(f"THE PRESENTING NUM OF BYTES IS EQUAL To {presentNum}")
            
            encodedData=(next(data) for _ in range(dataSize))
            with open(fileName,"wb") as resultf:
                for byte in retransferData(encodedData,presentNum):
                    resultf.write(byte)
        except StopIteration:
            break
def encodeFile(files:List[str],resultFile=None):
    assert isinstance(files,list),"THE FILES MUST BE A LIST"
    if not resultFile:
        resultFile=os.path.splitext(os.path.basename(files[0]))[0]+".huf"
    transferDataFile([os.path.abspath(file)for file in files],resultFile)
    return resultFile
        
    
    
        
        