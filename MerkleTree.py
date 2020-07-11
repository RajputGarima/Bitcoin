from config import *
from HashAlgo import *
from Transaction import *


class MerkleTree:
    def __init__(self, child, txnflag = False):
        if(txnflag):
            self.hashVal = child[0].hashVal
        else:
            allHashVal = ""
            for i in child:
                allHashVal += i.hashVal
            j = arity - len(child)
            if j > 0:
                allHashVal += i.hashVal * j
            self.hashVal = generateHash(allHashVal)

        self.childs = child
        self.txn = txnflag


# t1 = Transaction('x','y','z')
# t2 = Transaction('y','z','t')

# m1 = MerkleTree([t1], "A", True)
# m2 = MerkleTree([t2],"B", True)

# m3 = MerkleTree([m1,m2],"C")

# t3 = Transaction('x','y','z')
# t4 = Transaction('y','z','t')

# m4 = MerkleTree([t3],"D", True)
# m5 = MerkleTree([t4],"E", True)

# m6 = MerkleTree([m4,m5],"F")

# m7 = MerkleTree([m3,m6],"G")
