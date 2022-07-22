from Binary_tree.Tree import Basic_Tree
from init_file import *
from random import randint
import os,io,inspect
from pycv2.tools.utils import createProgressBar,progressBar
class HuffmanTree(Basic_Tree):
    @property
    def repreBits(self):
        assert self.parent,f"there is no parent to the code {self.parent} {self}"
        return self._parent(self)
    @property
    def repreByte(self):
        bits=self.repreBits
        return "00000000"[len(bits):]+bits
    @staticmethod
    def _parent(node:Basic_Tree,orgbyte=""):
        if not node.parent:
            return orgbyte
        if id(node.parent.left)==id(node):
            return HuffmanTree._parent(node.parent,"1"+orgbyte)
        if id(node.parent.right)==id(node):
            return HuffmanTree._parent(node.parent,"0"+orgbyte)

# ensure it is byte representatio
def get_codec(data: Iterable[int])->dict:
    propabilites = dict()
    def add(byte: bytes):
        if byte in propabilites:
            propabilites[byte] += 1
        else:
            propabilites[byte]=1
    print("READING THE FILE")
    for byte in data:
        add(byte)
    size=sum(propabilites.values())
    bytesprop=list(map(lambda item:HuffmanTree(item[1]/size,value=item[0]),propabilites.items()))
    props=bytesprop.copy()
    while len(props)!=1:
        props.sort(reverse=True)
        left,right=props[-2:]  
        key=left.key+right.key
        newNode=Basic_Tree(key,None,left,right)
        for bst in [left,right]:
            bst.parent=newNode
            props.pop(-1)
        props.append(newNode)
    codec=dict()
    entropy=0
    for prop in bytesprop:
        codec[prop.value]=bits=prop.repreBits
        entropy+=len(bits)*prop.key
    return codec
def transferData(data:Iterable[int],codec:dict=None)-> bytes:
    encoding:dict=codec if codec else get_codec(data)
    code=""
    print("COMPRESSING THE FILE")
    for byte in data:
        code+=encoding[byte]
        if len(code)<8:
            continue
        byte_code=int(code[:8],2)
        code=code[8:]
        yield bytes([byte_code])
    while code:
        if len(code)<8:
            bitsCodecs=list(codec.values())
            while True:
                newcode=bin(randint(0,255))[2:]
                newcode="00000000"[len(newcode):]+newcode
                newcode=newcode[len(code):]
                for end in range(len(newcode)+1):
                    if newcode[:end] in bitsCodecs:
                        break
                else:
                    break

            code=code+newcode
        byte_code=int(code[:8],2)
        code=code[8:]
        yield bytes([byte_code])
def retransfer(data:Iterable[int],codec:dict)-> bytes:
    codec=dict({(value,str(key)) for key,value in codec.items() })
    def _getresult(binary:str):
        result_bytes=[]
        start=0
        for end in range(len(binary)+1):
            if binary[start:end] in codec:
                result_bytes.append(
                    int(codec[binary[start:end]])
                    )
                start=end
        return binary[start:],bytes(result_bytes)
    def search(byte: int,last_code):
        byte=bin(byte)[2:]
        _binary=last_code+"00000000"[len(byte):]+byte
        return _getresult(_binary)

    last_code=""
    for byte in data:
        last_code,resBytes=search(byte,last_code)
        yield resBytes
    print("DECODING FINISNHED PROPBABLY") 



def _getDataBytes(file,tickEvery=0.2)->bytes:
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
def _getData(file)->int:
    for byte in _getDataBytes(file):
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


def transferData_file(files:str,resultfile,codec:dict=None):
    files=files if isinstance(files,list) else [files]  
    assert( not resultfile in files) \
        ,"the orginal file and resultfile must be no same"
    org_size=0
    
    with open(resultfile,"wb") as resultf:
        resultf.write((0).to_bytes(2,"big"))
        n=0
        for dirFile in files:
            for dir in getAlldirs(dirFile):
                resultf.write(InitDir(dir))
                n+=1
        resultf.seek(0)
        resultf.write(n.to_bytes(2,"big"))
        resultf.seek(0,io.SEEK_END)
        
        for dirFile in files:
            cursor_now=resultf.tell()
            filesdir=getALLFiles(dirFile)
            filesCompletePath=getALLFiles(dirFile,False)
            for file,fileName in zip(filesCompletePath,filesdir):
                org_size+=os.stat(file).st_size
                codec=codec if codec else get_codec(_getData(file))
                sizeofbytes=0
                addedBytes=0
                for byte in encodeInitCompressData(0,fileName,codec):
                    resultf.write(byte)
                    addedBytes+=len(byte)
                for byte in transferData(_getData(file),codec):
                    resultf.write(byte)
                    sizeofbytes+=len(byte)
                addedBytes+=sizeofbytes
                resultf.seek(cursor_now)
                resultf.write(sizeofbytes.to_bytes(NUM_INIT_SIZE_BYTES,"big"))
                resultf.seek(0,io.SEEK_END)
       
    
    result_size=os.stat(resultfile).st_size
    print(f"the File redced by {round(100-(result_size/org_size)*100,2)}%")
@lastPath
def retransfer_file(file,resultPath="."):
    data=_getDataBytes(os.path.abspath(file))
    
    os.chdir(resultPath)
    for dir in decodeInitDirFile(data):
        if not os.path.exists(dir):
            os.makedirs(dir)
    while True:
        try:
            dataSize,fileName,codec=decodeInitCompressData(data)
            encodedData=(ord(next(data)) for _ in range(dataSize))
            with open(fileName,"wb") as resultf:
                for byte in retransfer(encodedData,codec):
                    resultf.write(byte)
        except StopIteration:
            break
    
def encodeFile(files:List[str],resultFile=None):
    assert isinstance(files,list),"THE FILES MUST BE A LIST"
    if not resultFile:
        resultFile=os.path.splitext(os.path.basename(files[0]))[0]+".huf"
    transferData_file([os.path.abspath(file)for file in files],resultFile)
    return resultFile

def __main():
    os.chdir("./testing")
    resultFile=encodeFile(["test_text.txt"])
    retransfer_file(resultFile)
    
def __test_longCompression():
    file_name=r"G:\Videos\[EgyBest].Gravity.2013.BluRay.240p.x264.mp4"
    resultFile=encodeFile([file_name],"./testing/resultVideo.huf")
    retransfer_file(resultFile,"./testing/")

if __name__ == "__main__":
    __test_longCompression()
    
    
    
