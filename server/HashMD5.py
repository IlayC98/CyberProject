import hashlib

def hash_pass(password):
    n=hashlib.md5(str(password).encode())
    hashp=n.digest()
    return hashp