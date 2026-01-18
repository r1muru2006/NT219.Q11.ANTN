from pwn import *
import time

import warnings
warnings.filterwarnings("ignore", category=BytesWarning)


BLOCK_SIZE = 16
COUNT = 0

def unpad(data, blocksize=BLOCK_SIZE):
    pad_len = data[-1]
    if data and pad_len < blocksize and data[-pad_len:] == bytes([pad_len]) * pad_len:
        return data[:-pad_len]
    return data


def single_block_attack(iv, ciphertext, oracle):
    after_decrypt = b""
    global COUNT
    for i in reversed(range(16)):
        padding = bytes([16 - i] * (16 - i))
        for ch in range(256):
            COUNT += 1
            _iv = bytes(i) + xor(padding, bytes([ch]) + after_decrypt)

            if oracle(_iv, ciphertext):
                after_decrypt = bytes([ch]) + after_decrypt
                break

    return xor(iv, after_decrypt)


def full_attack(iv, ciphertext, oracle):
    plaintext = b""
    print("\n------Starting the recovery process------")
    start = time.time()
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = single_block_attack(iv, ciphertext[i : i + BLOCK_SIZE], oracle)
        plaintext += block
        iv = ciphertext[i : i + BLOCK_SIZE]
        print(f'Successfully recovering block {i // 16 + 1}: {unpad(block, 16).decode()}')
    end = time.time()
    print("---DONE---\n")
    finish_time = end - start
    return plaintext, finish_time


context.log_level = "info"

HOST = "127.0.0.1"
PORT = 1337
io = remote(HOST, PORT)


def get_data():
    io.recvuntil(b": ")
    given = bytes.fromhex(io.recvline().strip().decode())
    iv, ct = given[:BLOCK_SIZE], given[BLOCK_SIZE:]
    return iv, ct


def check_service(iv, ct):
    send = (iv + ct).hex()
    io.sendlineafter(b": ", send)
    data = io.recvline().strip().decode()
    if "FAIL" in data:
        return False
    return True


if __name__ == "__main__":
    iv, ct = get_data()
    print("--------Let's break this server!!!--------")
    print(f"This is the initialization vector (hex): {iv.hex()}")
    print(f"This is the ciphertext (hex): {ct.hex()}")
    
    pt, time_taken = full_attack(iv, ct, check_service)
    flag = unpad(pt, 16)
    
    print(f"Total Oracle Requests: {COUNT} requests")
    print(f"Wall Time: {(time_taken):.4f} seconds\n")
    print(f"Here is the recovered data: {flag.decode(errors='ignore')}\n")
