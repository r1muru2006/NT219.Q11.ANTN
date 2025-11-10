# Week 3–4 Report — DES Brute-Force & AES Baseline
## 1. Objective
The objective for weeks 3–4 was to implement and evaluate a proof-of-concept (PoC) brute-force attack on DES/3DES (Experiment A) and to collect baseline performance metrics for AES encryption. Deliverables include reproducible scripts, measurement logs, and a short analysis.

## 2. Lab setup and tools
- **Host environment:** Ubuntu 22.04 LTS (or similar), Python 3.10+, pip.  
- **Libraries:** pycryptodome (`pip install pycryptodome`).  
- **Tools (optional for scaling):** Hashcat (GPU), NVIDIA drivers + CUDA, multiprocessing for CPU parallelization.  
- **Hardware used for measurement (example):** Laptop/VM with Intel i7, 16GB RAM. No GPU used in baseline demo.
- **Repository layout (relevant):**
## 3. Methodology
### 3.1 DES brute-force (PoC)
- Use PyCryptodome to encrypt a single 8-byte block with a known DES key.
- Implement a trial loop that iterates over a limited keyspace (demo uses 2^16 = 65536 trials) for reproducibility on consumer hardware.
- For each trial key: create DES cipher, decrypt ciphertext or encrypt plaintext, compare with expected value.
- Record elapsed time and found key (if any).

### 3.2 AES baseline
- Use AES-128 (PyCryptodome) to encrypt many blocks to measure throughput (1,000,000 blocks demo).
- Measure time and compute ops/sec.

## 4. Results (summary)
- Demo brute-force over 2^16 keys finds the key within ~0.5–1.5 seconds on commodity CPU (varies by CPU).
- Observed key search rate: ~50k–150k keys/sec depending on hardware.
- Extrapolating to full DES keyspace (2^56) shows infeasibility on CPU (would take many millennia).
- AES-128 baseline throughput: example result ~0.4–0.6 million blocks/sec on tested host (fast in software).

> **Conclusion:** The PoC confirms that small-space brute force is trivial for demonstration, while full 2^56 DES brute-force requires specialized hardware or large GPU clusters. AES remains impractical to brute-force; attacks must target implementation flaws.

## 5. Reproducibility & safety
- All experiments were run in an isolated lab environment using synthetic test vectors. **Do not** target real systems.
- All provided scripts operate on demo/test data only (see `data/demo_cipher.hex`).
- To reproduce:
  1. Create a Python virtual environment, `pip install pycryptodome`.
  2. Run `python experiments/exp_des_bruteforce/bruteforce_des.py`.
  3. Run `python scripts/benchmark_aes.py` to measure AES baseline.

## 6. Files added in Week 3–4
- `experiments/exp_des_bruteforce/bruteforce_des.py` — simple single-process demo.
- `experiments/exp_des_bruteforce/bruteforce_des_mp.py` — multiprocessing demo to split key ranges (CPU parallel).
- `experiments/exp_des_bruteforce/README.md` — run instructions and safety notes.
- `scripts/benchmark_aes.py` — AES encrypt benchmark.
- `data/demo_cipher.hex` — sample ciphertext (hex) used in demo.

## 7. Next steps
- Week 5–6: Implement padding oracle PoC (AES-CBC) in `experiments/exp_padding_oracle/`.
- If GPU resources are available, prepare Hashcat workflows and range-splitting helpers for scaling DES search.

---

**Author note:** This report is a reproducible summary of the initial implementation. See the `README.md` in `experiments/exp_des_bruteforce` for detailed commands and parameter tuning.
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
