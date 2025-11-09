# Tên file: attack.py
from pwn import *
from Crypto.Cipher import AES
import os 

context.log_level = 'debug'

HOST = "127.0.0.1"
PORT = 1337
io = remote(HOST, PORT)

def oracle(ct):
    io.recvuntil(b"Send ciphertext (hex):")
    io.sendline(ct.hex().encode()) 

if __name__ == "__main__":
    io.recvline()
    oracle()