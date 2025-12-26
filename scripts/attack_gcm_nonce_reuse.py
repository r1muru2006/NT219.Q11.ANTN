from Crypto.Util.number import long_to_bytes as lb
from Crypto.Util.number import bytes_to_long as bl
from Crypto.Util.Padding import pad
from sage.all import *
from pwn import *
import struct

def bytes_to_polynomial(block, a):
    poly = 0
    bin_block = bin(bl(block))[2:].zfill(128)
    for i in range(len(bin_block)):
        poly += a**i * int(bin_block[i])
    return poly


def polynomial_to_bytes(poly):
    return lb(int(bin(poly._integer_representation())[2:].zfill(128)[::-1], 2))


def convert_to_blocks(ciphertext):
    return [ciphertext[i : i + 16] for i in range(0, len(ciphertext), 16)]


def xor(s1, s2):
    if len(s1) == 1 and len(s1) == 1:
        return bytes([ord(s1) ^ ord(s2)])
    else:
        return bytes(x ^ y for x, y in zip(s1, s2))


P_temp = PolynomialRing(GF(2), name="x")
x_temp = P_temp.gen()
F, a = GF(
    2**128, name="a", modulus=x_temp**128 + x_temp**7 + x_temp**2 + x_temp + 1
).objgen()
R, x = PolynomialRing(F, name="x").objgen()

io = remote("localhost", 21337)
# io = process(['python3', '/home/r1muru/NT219.Q11.ANTN/experiments/exp_gcm_nonce_reuse/vuln.py'])

def enc_msg(plaintext):
    io.sendlineafter(b"Select option: ", b"1")
    io.sendlineafter(b"Enter the plaintext: ", plaintext.hex().encode())
    data = io.recvline()
    
    nonce = None
    if b"Nonce:" in data:
        nonce = bytes.fromhex(data.decode().strip().split(": ")[1])
    
    ciphertext = bytes.fromhex(
        io.recvline_contains(b"Ciphertext: ").decode().strip().split(": ")[1]
    )

    if b"Error" in data or nonce is None:
        return ciphertext, None, None
    tag = bytes.fromhex(io.recvline_contains(b"Tag: ").decode().strip().split(": ")[1])
    return ciphertext, tag, nonce


def dec_msg(ciphertext, tag):
    io.sendlineafter(b"Select option: ", b"2")
    io.sendlineafter(b"Enter the ciphertext: ", ciphertext.hex().encode())
    io.sendlineafter(b"and the tag: ", tag.hex().encode())
    data = io.recvline()
    if b'Error' in data:
        return None
    plaintext = bytes.fromhex(data.decode().strip().split(": ")[1])
    return plaintext


payload1 = b"A" * 32
payload2 = b"B" * 32
payload3 = pad(b"give me the flag", 32)

print("Encrypting payload 1...")
C1_result = enc_msg(payload1)
C1 = convert_to_blocks(C1_result[0])
T1 = C1_result[1]
print(f"Ciphertext 1: {(C1_result[0]).hex()}")
print(f"Tag 1: {T1.hex()}")

print("\nEncrypting payload 2...")
C2_result = enc_msg(payload2)
C2 = convert_to_blocks(C2_result[0])
T2 = C2_result[1]
print(f"Ciphertext 1: {(C2_result[0]).hex()}")
print(f"Tag 2: {T2.hex()}")

print("\nEncrypting payload 3...")
C3_result = enc_msg(payload3)
C3 = convert_to_blocks(C3_result[0])
print(f"Ciphertext 3: {(C3_result[0]).hex()}")

L = struct.pack(">QQ", 0 * 8, len(C1) * 8)
C1_p = [bytes_to_polynomial(C1[i], a) for i in range(len(C1))]
C2_p = [bytes_to_polynomial(C2[i], a) for i in range(len(C2))]
C3_p = [bytes_to_polynomial(C3[i], a) for i in range(len(C3))]
T1_p = bytes_to_polynomial(T1, a)
T2_p = bytes_to_polynomial(T2, a)
L_p = bytes_to_polynomial(L, a)
# Here G_1 is already modified to include the tag
G_1 = (C1_p[0] * x**3) + (C1_p[1] * x**2) + (L_p * x) + T1_p
G_2 = (C2_p[0] * x**3) + (C2_p[1] * x**2) + (L_p * x) + T2_p
G_3 = (C3_p[0] * x**3) + (C3_p[1] * x**2) + (L_p * x)
P = G_1 + G_2
auth_keys = [r for r, _ in P.roots()]
for H, _ in P.roots():
    EJ = G_1(H)
    T3 = G_3(H) + EJ
    calc_tag = polynomial_to_bytes(T3)
    print(f"\nTrying H: {H}")
    print(f"Calculated tag: {calc_tag.hex()}")
    try:
        plaintext = dec_msg(C3[0] + C3[1], calc_tag)
        print(f"Decrypted: {plaintext.hex()}")
        print(f"\nPLAINTEXT: {plaintext.decode()}")
    except:
        print(f"Decryption failed")
        continue