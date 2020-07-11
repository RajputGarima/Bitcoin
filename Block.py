from config import *
from HashAlgo import *

import sys


class Block:
    def __init__(self, prevBlockPtr, root, nonce, transactionList):
        self.prevBlockPtr = prevBlockPtr
        if(prevBlockPtr):
            self.prevBlockHash = prevBlockPtr.hashVal
        else:
            self.prevBlockHash = ""
        self.txnList = transactionList
        self.noOfTxn = len(transactionList)
        self.merkleTreeRoot = root
        self.nonce = nonce

        allHash = ""
        # allHash += root.hashVal + self.prevBlockHash + str(nonce) + str(self.noOfTxn)
        allHash += self.prevBlockHash + str(nonce) + str(self.noOfTxn) + self.merkleTreeRoot.hashVal
        self.hashVal = generateHash(allHash)

    def get_size(self):
        totalSize = 0
        totalSize += sys.getsizeof(self.prevBlockHash)
        totalSize += sys.getsizeof(self.nonce)
        totalSize += sys.getsizeof(self.hashVal)
        for txn in self.txnList:
            totalSize += txn.get_size()
        noOfNodesinMerkleTree = 15
        n = 15
        while(n>1):
            noOfNodesinMerkleTree += (n + arity - 1)//arity
            n = (n+ arity - 1)//arity
        totalSize += noOfNodesinMerkleTree * sys.getsizeof(self.merkleTreeRoot.hashVal)
        return totalSize




# b = None
# # print(sys.getsizeof(b))
# b1 = Block(None, None, 879796, [])
# # print(sys.getsizeof(b1))
# b2 = Block(b1,b1, 3000, [])
# b1.get_size()
# b2.get_size()
# print((9+3)//4)
