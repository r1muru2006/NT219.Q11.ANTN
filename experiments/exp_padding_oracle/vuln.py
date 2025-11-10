from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import sys
import os


FLAG = open("/flag", "r").read().encode()
KEY = os.urandom(16)
iv = os.urandom(16)
ct = AES.new(KEY, AES.MODE_CBC, iv).encrypt(pad(FLAG, 16))

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
        if len(ct) < AES.block_size * 2:
            print(b"Length of ciphertext not valid for CBC mode.")
            return
        
        pt = cbc_decrypt(ct)
        if pt.decode(errors='ignore') == FLAG:
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
    print("Here is the data given for you!!!")
    given = (iv + ct).hex()
    print(f'iv||ct: {given}')
    
    print("Now it's your turn to break this")
    while True:
        challenge()