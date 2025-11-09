from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sys
import os


KEY = os.urandom(16)
FLAG = open("/flag", "r").read()

# send iv||ct to decrypt
def cbc_decrypt(ct):
    iv = ct[:16]
    ct = ct[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)
    return unpad(pt, AES.block_size)


def challenge():
    ct = bytes.fromhex(input("Send ciphertext (hex): "))
    try:
        if ct < AES.block_size * 2:
            print(b"Length of ciphertext not valid for CBC mode.")
            return
        
        pt = cbc_decrypt(ct)
        if pt.decode() == FLAG:
            print(f"Correct! Here is your flag: {FLAG}")
        else:
            print("Nope, try again!")
    except ValueError:
        print("FAIL: Bad padding.")
    except Exception:
        print(f"FAIL: Invalid input.")
    sys.stdout.flush()

if __name__ == "__main__": 
    print("---Welcome to the Padding Oracle Challenge!---")
    while True:
        challenge()