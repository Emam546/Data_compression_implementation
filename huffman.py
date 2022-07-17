from Binary_tree.Tree import BST, Basic_Tree
from typing import *
import os,json
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
      
            
        
        
def get_codec(file: str):
    propabilites = dict()
    def add(byte: bytes):
        if ord(byte) in propabilites:
            propabilites[ord(byte)] += 1
        else:
            propabilites[ord(byte)]=1
    with open(file, "rb") as f:
        byte=f.read(1)
        while byte:
            add(byte)
            byte=f.read(1)
    size=os.stat(file).st_size
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
    codecs=dict()
    entropy=0
    for prop in bytesprop:
        codecs[prop.value]=bits=prop.repreBits
        entropy+=len(bits)*prop.key
    return codecs
def transfer_file(file,resultfile,codecs:dict=None):
    assert resultfile!=file,"the orginal file and resultfile must be no same"
    encoding:dict=codecs if codecs else get_codec(file)
    with open(resultfile,"wb") as resultf:
        with open(file,"rb") as f:
            byte=f.read(1)
            code=""
            while byte:
                while byte and len(code)<8:
                    code+=encoding[ord(byte)]
                    byte=f.read(1)
                
                byte_code=int(code[:8],2)
                resultf.write(bytes([byte_code]))
                code=code[8:]
            while code:
                print("LEAST",code)
                byte_code=int(code[:8],2)
                result=bin(byte_code)[2:]
           
                resultf.write(bytes([byte_code]))
                code=code[8:]
    with open(f"{resultfile}.keys","w") as f:
        json.dump(encoding,f)
    result_size=os.stat(resultfile).st_size
    org_size=os.stat(file).st_size
    print(f"the File redced by {round(100-(result_size/org_size)*100,2)}%")
def retransfer(file,result_file):
    assert file!=result_file,"the result file must be another file"
    codecsFile=f"{file}.keys"
    #assert not os.path.exists(codecsFile),f"the keys of the {codecsFile} doesn't exists"
    with open(codecsFile,"r") as f:
        codec=dict({(value,str(key)) for key,value in json.load(f).items()})
    def search(byte: bytes,last_code):
        byte=bin(ord(byte))[2:]
        binary=last_code+"00000000"[len(byte):]+byte
        result_bytes=[]
        start=0
        for end in range(1,len(binary)):
            if binary[start:end] in codec:
                result_bytes.append(
                    int(codec[binary[start:end]])
                    )
                start=end
        return binary[start:],bytes(result_bytes)
    with open(result_file,"wb") as resultFile:
        with open(file,"rb") as f:
            byte=f.read(1)
            last_code=""
            while byte:
                last_code,result_bytes=search(byte,last_code)
                resultFile.write(result_bytes)
                byte=f.read(1)
            if last_code:
                print(last_code)
                last_code,result_bytes=search(bytes([0]),last_code)
                print(last_code)
    print("DECODING FINISNHED PROPBABLY")        

def __main():
    transfer_file(r"./test_text.txt","./text_resultfile.txt")
    # #__test()
    retransfer("./text_resultfile.txt","final_result.txt")
if __name__ == "__main__":
    __main()
    
    
    
