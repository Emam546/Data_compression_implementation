from Binary_tree.Tree import Basic_Tree
from huff.init_file import *
from random import randint
import os,io,inspect
from __funct import *

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
    if not len(propabilites):
        return {};
    elif len(propabilites)==1:
        return {list(propabilites.keys())[0]:"0"}
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
def transferData(data:Iterable[int],codec:dict=None):
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
def retransferData(data:Iterable[int],codec:dict)-> bytes:
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
    print("DECODING FINISHED PROBABLY") 



def transferDataFile(files:str,resultfile,codec:dict=None):
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
                org_size+=os.stat(file).st_size
                codec=codec if codec else get_codec(getData(file))
                sizeofbytes=0
                for byte in encodeInitCompressData(0,fileName,codec):
                    resultf.write(byte)
                for byte in transferData(getData(file),codec):
                    resultf.write(byte)
                    sizeofbytes+=len(byte)

                resultf.seek(cursor_now)
                resultf.write(sizeofbytes.to_bytes(NUM_INIT_SIZE_BYTES,"big"))
                resultf.seek(0,io.SEEK_END)
    result_size=os.stat(resultfile).st_size
    print(f"the File reduced by {round(100-(result_size/org_size)*100,2)}%")
@lastPath
def retransferDataFile(data: Iterable[bytes],resultPath="."):
    os.chdir(resultPath)
    for dir in decodeInitDirFile(data):
        if not os.path.exists(dir):
            os.makedirs(dir)
    while True:
        try:
            dataSize,fileName,codec=decodeInitCompressData(data)
            encodedData=(ord(next(data)) for _ in range(dataSize))
            with open(fileName,"wb") as resultf:
                for byte in retransferData(encodedData,codec):
                    resultf.write(byte)
        except StopIteration:
            break
    
def encodeFile(files:List[str],resultFile=None):
    assert isinstance(files,list),"THE FILES MUST BE A LIST"
    if not resultFile:
        resultFile=os.path.splitext(os.path.basename(files[0]))[0]+".huf"
    transferDataFile([os.path.abspath(file)for file in files],resultFile)
    return resultFile

