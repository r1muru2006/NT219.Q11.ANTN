from Crypto.Cipher import AES
import os
import sys


KEY = os.urandom(16)
NONCE = os.urandom(16)
flag = open("/flag", "rb").read()

def encrypt():
    plaintext = bytes.fromhex(input("Enter the plaintext: "))
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=NONCE)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    if b"flag" in plaintext:
        print("Error: Invalid plaintext, not authenticating", flush=True)
        print("Ciphertext:", ciphertext.hex(), flush=True)
    else:
        print("Nonce:", NONCE.hex(), flush=True)
        print("Ciphertext:", ciphertext.hex(), flush=True)
        print("Tag:", tag.hex(), flush=True)


def decrypt():
    c_hex = input("Enter the ciphertext: ")
    t_hex = input("and the tag: ")

    ct = bytes.fromhex(c_hex)
    tag = bytes.fromhex(t_hex)

    cipher = AES.new(KEY, AES.MODE_GCM, nonce=NONCE)
    try:
        decrypted = cipher.decrypt_and_verify(ct, tag)
    except ValueError as e:
        print("Error: Invalid authentication tag", flush=True)
        return

    if b"give me the flag" in decrypted:
        print("Plaintext:", flag.hex(), flush=True)
    else:
        print("Plaintext:", decrypted.hex(), flush=True)



if __name__ == "__main__":

    options = """
Welcome to the AES-GCM encryption and decryption tool!
    1. Encrypt message
    2. Decrypt message
    """

    menu = {"1": encrypt, "2": decrypt}

    while True:
        print(options, flush=True)
        choice = input("Select option: ").strip()

        if choice not in menu.keys():
            print("Not a valid choice...", flush=True)
            continue

        menu[choice]()
