from BitcoinScripts import *
from config import *
from HashAlgo import *
import sys
from Crypto.Hash import SHA256
from prettytable import PrettyTable


class Transaction:

    def __init__(self, prev_txn, scriptSign, amnt, receiverPubKeyHash, genesisBlockTxn = False):
        allHash = ""
        for txn in prev_txn:
            allHash += txn[0].hashVal + str(txn[1])
        #self.input = [((txn,index),scriptsignature), ...]
        self.input = list(zip(prev_txn, scriptSign))
        self.validTxn = True
        # self.output = [(value, scriptPubKEy), ... ]
        self.output = []
        if(genesisBlockTxn):
            self.output.append((amnt, ScriptPubKey(receiverPubKeyHash, receiverPubKeyHash.hexdigest())))
            for res in self.output:
                allHash += str(res[0]) + res[1].publicKeyHash.hexdigest()
            self.hashVal = generateHash(allHash)
            receiverPubKeyHash.update(self.hashVal.encode())
            return
        validCoins = self.isValidTxn(amnt)
        if validCoins == -1:
            self.hashVal = generateHash(allHash)
            self.validTxn = False
            return

        self.output.append((amnt, ScriptPubKey(receiverPubKeyHash, receiverPubKeyHash.hexdigest())))
        if validCoins > amnt:
            for val in self.input:
                wallet_amt = val[0][0].output[val[0][1]][0]
                paid_amt = 0
                if amnt > 0:
                    paid_amt = min(wallet_amt,amnt)
                    wallet_amt -= paid_amt
                    amnt -= paid_amt
                if(wallet_amt > 0):
                    senderPubKeyHash = SHA256.new(hashlib.sha256(val[1].pubKey).hexdigest().encode())
                    self.output.append((wallet_amt, ScriptPubKey(senderPubKeyHash, senderPubKeyHash.hexdigest())))

        for res in self.output:
            allHash += str(res[0]) + res[1].publicKeyHash.hexdigest()
        self.hashVal = generateHash(allHash)

        for opt in self.output:
            opt[1].publicKeyHash.update(self.hashVal.encode())



    def isValidTxn(self, amnt):
        validBitCoins = 0
        for x in self.input:
            index = x[0][1]
            txnhash = x[0][0].hashVal
            scriptSign = x[1]
            scriptpubKey = x[0][0].output[index][1]
            if executeScripts(scriptSign, scriptpubKey, txnhash) == False:
                return -1
            validBitCoins += x[0][0].output[index][0]
        if validBitCoins < amnt:
            return -1
        return validBitCoins
    
    def get_size(self):
        totalSize = 0
        totalSize += sys.getsizeof(self.hashVal)
        totalSize += sys.getsizeof(self.input)
        totalSize += sys.getsizeof(self.output)
        return totalSize



# senderkey = RSA.generate(2048)
# senderpubKey = senderkey.publickey().exportKey('PEM')
# senderpvtKey = senderkey.exportKey('PEM')

# sdrpubkeyhobj = SHA256.new(hashlib.sha256(senderpubKey).hexdigest().encode())
# sendrpubKeyhash = sdrpubkeyhobj.hexdigest()

# recvrkey = RSA.generate(2048)
# recvrpubKey = recvrkey.publickey().exportKey('PEM')
# recvrpvtKey = recvrkey.exportKey('PEM')
# recvrpubKeyHash = SHA256.new(hashlib.sha256(recvrpubKey).hexdigest().encode())


# txn = Transaction([],[],50,sdrpubkeyhobj,None,True)
# senderPrevTxn = [(txn , 0)]



# signer = PKCS115_SigScheme(RSA.importKey(senderpvtKey))
# sendersignature = signer.sign(sdrpubkeyhobj)


# txn1 = Transaction(senderPrevTxn,[ScriptSign(sendersignature,senderpubKey)], 50, recvrpubKeyHash, sdrpubkeyhobj)
