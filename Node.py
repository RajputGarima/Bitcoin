import concurrent.futures
import multiprocessing
import threading
import time
from random import random, randrange

from Crypto.PublicKey import RSA

from Block import *
from Blockchain import *
from config import *
from MerkleTree import MerkleTree
from Transaction import *
from prettytable import PrettyTable


class Node:
    allNodes = []
    txnFlag = True
    txnnodes = []
    txns_performed = PrettyTable()
    txns_performed.field_names = ["Sender ", "Receiver ", "Amount ", "Valid"]
    # publicKeyMap = {hash --> id}
    publickeyMap = {}

    def __init__(self, id):
        self.id = id
        self.pubKey = []
        self.pvtKey = []
        self.blockchain = BlockChain()
        for i in range(5):
            key = RSA.generate(2048)
            self.pubKey.append(key.publickey().exportKey('PEM'))
            self.pvtKey.append(key.exportKey('PEM'))
            pubKeyHash = SHA256.new(hashlib.sha256(self.pubKey[i]).hexdigest().encode())
            Node.publickeyMap[pubKeyHash.hexdigest()] = str(self.id) +  " . " + str(i)

        self.transactions = []
        self.blockqueue = []
        self.target = None
        self.incentive = 0
        self.bitcoins = 0
        self.start = 0
        # self.utxo = {pubKeyHash: [(transactionHashPtr, transactionIndex), ... ] , .. }
        self.utxo = {}

    def getWalletAddress(self):
        keyno = randrange(0,5)
        pubKey = self.pubKey[keyno]
        keyhash = SHA256.new(hashlib.sha256(pubKey).hexdigest().encode())
        return keyhash

    def run(self):
        self.start = time.time()
        while(True):
            end = time.time()
            if(end - self.start > 15):
                if(len(self.transactions) > 0):
                    timer = time.time()
                    blk = self.createBlock()
                    self.target = blk.hashVal
                    pow = self.proofOfWork()
                    if pow:
                        Node.txnFlag = False

                        flag = True
                        for node in self.allNodes:
                            if node.getConsensus(blk) == False:
                                flag = False
                                break

                        if flag:
                            print("---------------------- Transactions Performed --------------------------")
                            print(Node.txns_performed)
                            Node.txns_performed.clear_rows()

                            print(" -------------------------------------------------------------------------- ")
                            for node in self.allNodes:
                                node.processBlocks(blk)
                            print("--------After Performing the Transaction final state of the Nodes---------")
                            self.printUTXO()

                            print("------------------------ Transactions Executed----------------------------")
                            self.printTxn(blk.txnList)

                            print(" -------------------------------------------------------------------------- ")
                            
                            Node.txnFlag = True
                            Node.txnnodes = []
                            self.incentive += incentive
                            randkeyno = randrange(0,5)
                            recverpubkeyHash = SHA256.new(hashlib.sha256(self.pubKey[randkeyno]).hexdigest().encode())
                            txn = Transaction([],[],incentive,recverpubkeyHash,True)
                            for node in self.allNodes:
                                node.processTransactions(txn)
                        else:
                            self.transactions = []
                            Node.txnFlag = True
                            Node.txnnodes = []
                    else:
                        self.start = time.time()


            dotxn = random()

            if(dotxn <= 0.2 and Node.txnFlag and self.id not in Node.txnnodes):
                recvr = randrange(0,numberOfNodes)
                while(str(recvr) == str(self.id)):
                    recvr = randrange(0,numberOfNodes)
                recvrnode = self.allNodes[recvr]
                recvrkeyhash = recvrnode.getWalletAddress()
                prev_txn = []
                scriptsign = []
                for j in range(5):
                    pkey = self.pubKey[j]
                    pvtkey = self.pvtKey[j]

                    try:
                        sendrpubkeyhash =  SHA256.new(hashlib.sha256(pkey).hexdigest().encode())
                        txn_l = self.utxo[sendrpubkeyhash.hexdigest()]
                        for t in txn_l:
                            sendrPubKeyHash =  SHA256.new(hashlib.sha256(pkey).hexdigest().encode())
                            sendrPubKeyHash.update(t[0].hashVal.encode())
                            signer = PKCS115_SigScheme(RSA.importKey(pvtkey))
                            sendersignature = signer.sign(sendrPubKeyHash)
                            prev_txn.append(t)
                            scriptsign.append(ScriptSign(sendersignature, pkey))
                    except KeyError:
                        continue
                bitcoinval = randrange(10,201)
                tempReceiver = recvrkeyhash.hexdigest()
                new_txn = Transaction(prev_txn,scriptsign,bitcoinval,recvrkeyhash)
                Node.txns_performed.add_row([self.id, Node.publickeyMap[tempReceiver], bitcoinval, new_txn.validTxn] )
                

                
                if new_txn.validTxn:
                    Node.txnnodes.append(self.id)
                for node in self.allNodes:
                    node.processTransactions(new_txn)
            time.sleep(1)

    def getConsensus(self, block):
        if self.blockchain.latestBlock != block.prevBlockPtr:
            return False
        for txn in block.txnList:
            if txn.validTxn == False:
                return False
            for inp in txn.input:
                sign = inp[1].pubKey
                signHash =  SHA256.new(hashlib.sha256(sign).hexdigest().encode())
                txn = inp[0]
                try:
                    if txn not in self.utxo[signHash.hexdigest()]:
                        return False
                except KeyError:
                    return False

        return True

    def generateNonce(self):
        return randrange(0,2**sizeOfNonce)

    def processTransactions(self, txn):
        if(txn.validTxn):
            self.transactions.append(txn)

    def processBlocks(self,blck):
        if(self.blockchain.rootBlock == None):
            self.blockchain.rootBlock = blck

        self.blockchain.latestBlock = blck
        temputxo = {}
        for txns in blck.txnList:
            for x in txns.input:
                index = x[0][1]
                scriptpubKey = x[0][0].output[index][1].recvrkeyHash
                try:
                    self.utxo[scriptpubKey] = []
                except KeyError:
                    continue
            index = 0
            for x in txns.output:
                scriptpubKey = x[1].recvrkeyHash
                try:
                    temputxo[scriptpubKey].append((txns,index))
                except KeyError:
                    temputxo[scriptpubKey] = [(txns, index)]
                index += 1

            try:
                self.transactions.remove(txns)
            except ValueError:
                continue
        for key in temputxo:
            val = temputxo[key]
            for j in val:
                try:
                    self.utxo[key].append(j)
                except KeyError:
                    self.utxo[key] = [j]
        self.start = time.time()

    def createGenesisBlock(self):
        bitcoinvalue = 1000
        for _ in range(numberOfNodes):
            randomNo = randrange(0,numberOfNodes)
            randkeyno = randrange(0,5)
            node = self.allNodes[randomNo]
            recverpubkeyHash = SHA256.new(hashlib.sha256(node.pubKey[randkeyno]).hexdigest().encode())
            t1 = Transaction([],[],bitcoinvalue,recverpubkeyHash,True)
            self.transactions.append(t1)
        txn = self.transactions.copy()
        rootMerkleTree = self.generateMerkleTree(txn)
        blk = Block(None,rootMerkleTree,self.generateNonce(),txn)
        for node in self.allNodes:
            node.processBlocks(blk)

        self.transactions = []


    def createBlock(self):
        start_time = time.time()
        txn = self.transactions.copy()
        rootMerkleTree = self.generateMerkleTree(txn)
        blk = Block(self.blockchain.latestBlock,rootMerkleTree,self.generateNonce(),txn)
        return blk


    def generateMerkleTree(self, txns):
        start_time = time.time()
        childs = []
        for i in txns:
            childs.append((MerkleTree([i],True),0))
        while(len(childs) > 1):
            level = childs[0][1]
            merkleTreeChild = []
            for i in range(arity):
                if(len(childs) > 0 and childs[0][1] == level):
                    merkleTreeChild.append(childs[0][0])
                    childs.remove(childs[0])

            childs.append((MerkleTree(merkleTreeChild),level+1))
        return childs[0][0]

    def proofOfWork(self):
        for node in self.allNodes:
            if(node.target is not None and self.target > node.target):
                return False
            if(self.id != node.id and self.target == node.target and self.id > node.id):
                return False
        return True

    def printTxn(self, txn_list):
        txns_executed = PrettyTable()
        txns_executed.field_names = ["ID" , "IN/OUT" ,"Wallet ID", "Amount"]
        for i in range(len(txn_list)):
            for inp in txn_list[i].input:
                wallet_amt = inp[0][0].output[inp[0][1]][0]
                pubKeyHash = SHA256.new(hashlib.sha256(inp[1].pubKey).hexdigest().encode())
                txns_executed.add_row([i, "IN", Node.publickeyMap[pubKeyHash.hexdigest()], wallet_amt])
            for otp in txn_list[i].output:
                wallet_amt = otp[0]
                pubKeyHash = otp[1].recvrkeyHash
                txns_executed.add_row([i, "OUT", Node.publickeyMap[pubKeyHash], wallet_amt])
        print(txns_executed)
        
    def printUTXO(self):

        x = PrettyTable()

        x.field_names = ["Node ID", "Wallet 0", "Wallet 1", "Wallet 2", "Wallet 3","Wallet 4"]
        for node in Node.allNodes:
            row = [node.id]
            for i in range(5):
                pubKeyHash = SHA256.new(hashlib.sha256(node.pubKey[i]).hexdigest().encode())
                amt = 0
                try:
                    val = self.utxo[pubKeyHash.hexdigest()]
                    for txn,ind in val:
                        amt += txn.output[ind][0]
                except KeyError:
                    amt += 0
                row.append(amt)
            x.add_row(row)
        print(x)
        print("--------------------------------------------------------------------------------")

def run_thread(node):
    node.run()


nodesList = []
for i in range(numberOfNodes):
    n1 = Node(i)
    nodesList.append(n1)
    n1.allNodes.append(n1)

nodesList[0].createGenesisBlock()

print("--------After Creating Genesis Block Initial State of the Nodes---------")
nodesList[0].printUTXO()

with concurrent.futures.ThreadPoolExecutor(max_workers=numberOfNodes) as executor:
        for node in nodesList:
            executor.submit(run_thread,node)
