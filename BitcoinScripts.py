import hashlib

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
# from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Signature.PKCS1_v1_5 import PKCS115_SigScheme


class ScriptPubKey:

    def __init__(self, publicKeyHash, recvrkeyHash):
        self.publicKeyHash = publicKeyHash
        self.recvrkeyHash = recvrkeyHash

class ScriptSign:

    def __init__(self, sign, publickey):
        self.sign = sign
        self.pubKey = publickey


def executeScripts(scriptSign, scriptPubKey, hashVal):
    signature = scriptSign.sign
    sigPubKey = scriptSign.pubKey
    pubKeyHash = scriptPubKey.publicKeyHash
    genpubKeyHash = SHA256.new(hashlib.sha256(sigPubKey).hexdigest().encode())
    genpubKeyHash.update(hashVal.encode())
    if(pubKeyHash.hexdigest() != genpubKeyHash.hexdigest()):
        return False
    verifier = PKCS115_SigScheme(RSA.importKey(sigPubKey))
    try:
        verifier.verify(pubKeyHash, signature)
    except:
        return False
    return True



# key = RSA.generate(2048)
# pubKey = key.publickey().exportKey('PEM')
# pvtKey = key.exportKey('PEM')
# hash = SHA256.new(hashlib.sha256(pubKey).hexdigest().encode())
# # print(hash.hexdigest())
# signer = PKCS115_SigScheme(RSA.importKey(pvtKey))
# signature = signer.sign(hash)
# key2 = RSA.generate(2048)
# pubKey2 = key2.publickey().exportKey('PEM')
# hash2 = SHA256.new(hashlib.sha256(pubKey2).hexdigest().encode())
# s = ScriptSign(signature, pubKey)
# scrptp = ScriptPubKey(hash2)
# print(executeScripts(s,scrptp))
