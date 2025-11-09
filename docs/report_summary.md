# Padding Oracle Experiment — Summary


## Objective
Demonstrate CBC-PKCS7 padding oracle, measure resources, and patch.


## Method
- Deployed vulnerable AES-CBC server (distinct error on bad padding).
- Attacker script uses oracle to recover plaintext block-by-block.
- Metrics: number of requests, time per block, retries.


## Results (example)
- Ciphertext blocks: 3 (IV + 2 data blocks)
- Total oracle requests: 7680 (approx)
- Wall time: ~2 minutes on localhost


## Patch & Retest
- Applied Encrypt-then-MAC (HMAC-SHA256): oracle removed; attack fails.
- Applied AES-GCM: attack fails; provides confidentiality+integrity.


## Recommendations
1. Use AEAD (AES-GCM / ChaCha20-Poly1305) for protocols.
2. If CBC must be used, adopt Encrypt-then-MAC and constant-time generic errors.
3. Log attempts and rate-limit decryption endpoints.