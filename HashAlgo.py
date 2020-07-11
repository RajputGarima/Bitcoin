import hashlib
from config import hashSize
 
def generateHash(message):
    result = "" 
    if hashSize == 224:
         result = hashlib.sha224(message.encode())
    elif hashSize == 256:
        result = hashlib.sha256(message.encode())
    elif hashSize == 384:
        result = hashlib.sha384(message.encode())
    else:
        result = hashlib.sha512(message.encode())
    return result.hexdigest()
