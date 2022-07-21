from Binary_tree.Tree import Basic_Tree
from inti_file import *
from random import randint
import os,json
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
            print("LEAST",code)
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
            print(f"final byte {code}")
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
    if last_code:
        print(f"the file ended with last_code {last_code}")
    print("DECODING FINISNHED PROPBABLY") 




def _getData(file)->int:
    with open(file,"rb") as f:
        for _ in progressBar(range(os.stat(file).st_size)):
            byte=f.read(1)
            yield ord(byte)
         
         
def transferData_file(file,resultfile,codec:dict=None):
    assert os.path.isfile(file) and resultfile!=file,"the orginal file and resultfile must be no same"
    codec=codec if codec else get_codec(_getData(file))
    
    
    with open(resultfile,"wb",buffering=9) as resultf:
        for byte in transferData(_getData(file),codec):
            resultf.write(byte)
    with open(f"{resultfile}.keys","w") as f:
        json.dump(codec,f)
    result_size=os.stat(resultfile).st_size
    org_size=os.stat(file).st_size
    print(f"the File redced by {round(100-(result_size/org_size)*100,2)}%")
def retransfer_file(file,result_file):
    assert file!=result_file,"the result file must be another file"
    codecsFile=f"{file}.keys"
    #assert not os.path.exists(codecsFile),f"the keys of the {codecsFile} doesn't exists"
    with open(codecsFile,"r") as f:
        codec=json.load(f)
        

    with open(result_file,"wb",buffering=9) as resultFile:
        for byte in retransfer(_getData(file),codec):
            resultFile.write(byte)
   
def __main():
    transferData_file("./test_text.txt","./text_resultfile.txt")
    # #__test()
    retransfer_file("./text_resultfile.txt","final_result.txt")
    with open("final_result.txt","r") as f1:
        with open("./test_text.txt","r") as f2:
            state=f1.read()==f2.read()
            if not state:
                print("files are not the same")
def test_longCompression():
    import os
    file_name=r"G:\Videos\[EgyBest].District.9.2009.BluRay.240p.x264.mp4"
    compress_path=os.path.splitext(file_name)[1]+'.huf'
    result_file="res.py"

def __test_encding():
    codec=list(get_codec(_getData("./test_text.txt")).values())
    for code in codec:
        start=0
        for end in range(len(code)):
            code
if __name__ == "__main__":
    __main()
    
    
    
