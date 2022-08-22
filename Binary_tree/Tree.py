
# Insert - O(log N) + O(N) = O(N)
                    #O(N) in organizing in every insert
# Find - O(log N)
# Update - O(log N)
# List all - O(N)

class Basic_Tree():
    def __init__(self, key,parent=None,left=None,right=None,value=None):
        self.key = key
        self.left = left
        self.right = right
        self.value=value
        self.parent=parent

    def __lt__(self, value):
        if isinstance(value,Basic_Tree):
            return self.key<value.key
        return False
    def __le__(self, value,):
        if isinstance(value,Basic_Tree):
            return self<value or self==value
        return False
    def __gt__(self, value):
        if isinstance(value,Basic_Tree):
            return self.key>value.key
        return True
    def  __ge__(self, value):
        if isinstance(value,Basic_Tree):
            return self>value or self==value
        return True
    def __eq__(self,value):
        if isinstance(value,Basic_Tree):
            return self.key==value.key
        return False
    def to_tuple(self):
        if not isinstance(self,Basic_Tree):
            return self
        if not isinstance(self.left,Basic_Tree) and not isinstance(self.right,Basic_Tree):
            return self.key
        return Basic_Tree.to_tuple(self.left),  self.key, BST.to_tuple(self.right)
    
    def __str__(self):
        return "BinaryTree <{}>".format(self.to_tuple())

    def __repr__(self):
        return "BinaryTree <{}>".format(self.to_tuple())
    @staticmethod
    def parse_tuple(data,parent=None):
        # print(data)
        if isinstance(data, tuple) and len(data) == 3:
            node = Basic_Tree(data[1],parent)
            node.left = Basic_Tree.parse_tuple(data[0],node)
            node.right = Basic_Tree.parse_tuple(data[2],node)
        elif data is None:
            node = None
        else:
            node = Basic_Tree(data,parent)
        return node

    def __bool__(self):
        return True

class BST(Basic_Tree):
    def _height(self):
        if not isinstance(self,Basic_Tree):
            return 0
        return 1 + max(BST._height(self.left), BST._height(self.right))
    @property
    def height(self):
        
        return self._height()
    def __len__(self):
        return self.size()
    def __iter__(self):
        return  (x for x in self.list_all())
    def size(self):
        if self is None:
            return 0
        return 1 + BST.size(self.left) + BST.size(self.right)

    def traverse_in_order(self):
        if self is None: 
            return []
        return (BST.traverse_in_order(self.left) + 
                [self.key] + 
                BST.traverse_in_order(self.right))
    def traverse_in_postorder(self):
        if self is None: 
            return []
        return (BST.traverse_in_postorder(self.left) + 
                BST.traverse_in_postorder(self.right)+
                [self.key])
    def travers_in_preorder(self):
        if self is None: 
            return []
        return ([self.key]+
                BST.travers_in_preorder(self.left) + 
                BST.travers_in_preorder(self.right)
                )
    @staticmethod
    def display_keys(self:Basic_Tree, space='\t', level=0):
        # If the node is empty
        if self is None:
            print(space*level + '∅')
            return   

        # If the node is a leaf 
        if self.left is None and self.right is None:
            print(space*level + str(self.key))
            return

        # If the node has children
        BST.display_keys(self.right, space, level+1)
        print(space*level + str(self.key))
        BST.display_keys(self.left,space, level+1)    
    
    
    def check_binary_tree_searching(self):
        if self.right !=None:
            return self.right.key<self.key and self.right.check_binary_tree_searching()
        return True
    def getmaxiumum_key(self):
        if not isinstance(self,BST):
            return 0
        _list=[self,]
        if isinstance(self.left,Basic_Tree):
            _list.append(self.left.getmaxiumum_key())
        if isinstance(self.right,Basic_Tree):
            _list.append(self.right.getmaxiumum_key())
        return max(_list)
    def getminiumum_key(self):
        if not isinstance(self,Basic_Tree):
            return None
        #we but lararge number to don't count it
        _list=[self,]
        if isinstance(self.left,Basic_Tree):
            _list.append(self.left.getminiumum_key())
        if isinstance(self.right,Basic_Tree):
            _list.append(self.right.getminiumum_key())
        return min(_list)
    @staticmethod
    def find(node: Basic_Tree, key):
        if node is None:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return BST.find(node.left, key)
        if key > node.key:
            return BST.find(node.right, key)
    def update(node, key, value):
        target = BST.find(node, key)
        if target is not None:
            target.value = value
    
    def list_all(node):
        if node is None:
            return []
        return BST.list_all(node.left) + [(node.key, node.value)] + BST.list_all(node.right)
    @property
    def width(self)->int:
        return 2**(self.height-1)
    def balance_bst(self):
        return self.make_balanced_bst(self.list_all())
    @staticmethod
    def is_balanced(node):
        if not isinstance(node,BST):
            return True, 0
        balanced_l, height_l = BST.is_balanced(node.left)
        balanced_r, height_r = BST.is_balanced(node.right)
        balanced = balanced_l and balanced_r and abs(height_l - height_r) <=1
        height = 1 + max(height_l, height_r)
        return balanced, height
    def insert(node, key, value):
        if node is None:
            node = BST(key, value=value)
        elif key < node:
            node.left = BST.insert(node.left, key, value)
            node.left.parent = node
        elif key > node:
            node.right = BST.insert(node.right, key, value)
            node.right.parent = node
        return node
    def update(node, key, value):
        target = BST.find(node, key)
        if target is not None:
            target.value = value
    # Ensure that the left subtree is balanced.
    # Ensure that the right subtree is balanced.
    # Ensure that the difference between heights of left subtree and right subtree is not more than 1.
    
    def is_full(self):
        #all the nodes has 2 or a zero children nodes
        if self!=None:
            if  BST.is_full(self.left) and BST.is_full(self.left):
                return True
            elif not BST.is_full(self.left) and not BST.is_full(self.left):
                #check if they are both are empty
                return True
            else:
                return False
        else:
            return False
    def is_perfect(self):
        return self.max_number_node()==self.size()
    def is_complete(self):
        #check if the tree is weel competed
        if isinstance(self,Basic_Tree):
            left_side=BST.is_complete(self.left)  
            right_side=BST.is_complete(self.right)
            if left_side ==True:
                return True
            elif left_side==None and right_side==None:
                return True
            else:
                return False
        else:
            return None
        

    # @staticmethod
    # def make_balanced_bst(data, lo=0, hi=None, parent=None):
    #     if hi is None:
    #         hi = len(data) - 1
    #     if lo > hi:
    #         return None
        
    #     mid = (lo + hi) // 2
    #     key, value = data[mid]

    #     root = BST(key, value)
    #     root.parent = parent
    #     root.left = make_balanced_bst(data, lo, mid-1, root)
    #     root.right = make_balanced_bst(data, mid+1, hi, root)
        
    #     return root

    #not acurate_way    
    def is_binary_search(self):
        #checking if its empty or not
        #not accurate
        if self is None:
            return True
        state=True
        if self.left!=None:
            if self.left>self:
                state=False
            elif not BST.is_binary_search(self.left):
                state=False
        if state and self.right!=None:
            #if they are any repeating in data
            if self.right<=self:
                state=False
            elif not BST.is_binary_search(self.left):
                state=False
        return state
    #overwrite this previous method

    def is_binary_search(self):
        #print("___new method")
        if self  >  BST.getminiumum_key(self.right):
            return False
        if self  <=  BST.getmaxiumum_key(self.right):
            return False   
        return True

    def parse_tuple(data,parent=None):
        # print(data)
        if isinstance(data, tuple) and len(data) == 3:
            node = BST(data[1],parent)
            node.left = BST.parse_tuple(data[0],node)
            node.right = BST.parse_tuple(data[2],node)
        elif data is None:
            node = None
        else:
            node = BST(data,parent)
        return node

    @staticmethod
    def parse_tuple(data,parent=None):
        # print(data)
        if isinstance(data, tuple):
            if len(data) == 3:
                node = BST(data[1],parent)
                node.left = BST.parse_tuple(data[0],node)
                node.right = BST.parse_tuple(data[2],node)
            elif len(data)==2:
                node = BST(data[0],parent,value=data[1])
            else:
                raise "undefined tuple"
        elif data is None:
            node = None
        return node

    def delete(self,value):
        node=self.find(value)!=None
        if node==None:return
        sticked_node=None
        if node.left==None and node.right==None:
            sticked_node=None
        elif self.left==None and self.right!=None:
            sticked_node=self.right
        elif self.left!=None and self.right==None:
            sticked_node=self.left
        else:
            #if they are both are emty
            sticked_node=self.right.getminiumum_key()
            #in case of repeating same key we will not apply recusion

            #theres is no need to check whethere it is right or left .
            sticked_node.parent.right=sticked_node.right
        if self.parent!=None:
            if self==self.parent.right:
                self.parent.right=sticked_node 
            else:
                self.parent.left=sticked_node
        elif sticked_node is None:
            raise "you can't make the tree empty"


if __name__=="__main__":
    example_tuple=(((-1,-1,0),1,2),3,(4,5,(7,8,9)))
    un_balanced=((0,1,2),3,(4,5,(7,8,9)))
    un_binary_search=((2,1,0),3,(4,5,6))
    un_is_complete=((None,1,(1.5,0,2.5)),3,(4,5,6))
    empty_list=(2)
    for _tuple in [example_tuple,un_balanced,un_binary_search,un_is_complete,empty_list]:
        tree=BST.parse_tuple(_tuple)
        #print("is_full :", tree.is_full())
        # print("is_complete :",tree.is_complete())
        print("is_balanced :",tree.is_balanced())
        print("is_perfect :",tree.is_perfect())
        print("is_binary_search :",tree.is_binary_search())

        print("size",tree.size())
        print("height",tree.height())
        print("width",tree.width())
        print("max value",tree.getmaxiumum_key())
        print("min value",tree.getminiumum_key())
        print("__________________________")

# insert(tree, biraj.username, biraj)
# insert(tree, sonaksh.username, sonaksh)
# insert(tree, aakash.username, aakash)
# insert(tree, hemanth.username, hemanth)
# insert(tree, siddhant.username, siddhant)
# insert(tree, vishal.username, siddhant)