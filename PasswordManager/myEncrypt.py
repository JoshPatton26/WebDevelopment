# ||||=====  Password Generator and Manager  =====||||
# Sources:
# https://www.youtube.com/watch?v=GYCVmMCRmTM
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
# https://www.geeksforgeeks.org/python-sqlite/
# ===================================================================

import random
import string
from Crypto.Cipher import AES
from secrets import token_bytes
import sqlite3 as sql

PASSLEN = 16
KEY = token_bytes(PASSLEN)

# Implementing AES 128 bit key encryption 
# Function takes  the plain text as an arg, encrypts the text using nonce, 128 bit key, using EAX mode.
# To call the function use: a, b, c = encrypt(val)
def a28(val):
    cipher = AES.new(KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    enc, tag = cipher.encrypt_and_digest(val.encode('ascii'))
    # print("\nEncrypted password: ", enc.decode(encoding='cp437', errors='strict')) # 
    # b82(nonce, enc, tag)
    return nonce, enc, tag
    
# Implementing AES decryption
# Function takes three args, all three are returned from encrypt() function above ^^
# To call the function use: d = decrypt(a, b, c)
def z82(nonce, enc, tag):
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    dec = cipher.decrypt(enc)
    try:
        cipher.verify(tag)
        # print("\nDecrypted password: ", dec.decode('ascii'))
        return dec.decode('ascii')
    except:
        return False
