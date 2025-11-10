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
# DES Brute-Force Attack Setup

- To demonstrate the feasibility and cost of brute-forcing the DES cipher, we designed a controlled experiment using both CPU-based Python scripts and GPU-accelerated Hashcat. The setup replicates a realistic scenario where the attacker possesses a known plaintext–ciphertext pair and attempts to recover the original 56-bit DES key.

## 1. Environment

Host OS: Ubuntu 22.04 LTS (or Windows 10 with WSL)

Python Version: 3.10+ with pycryptodome for DES encryption

GPU (optional): NVIDIA RTX 3060 / 3090 (or similar) for Hashcat acceleration

Hashcat Version: v6.2.6 or later

## 2. Known Data (Attack Input)

Generate an 8-byte plaintext and encrypt it with a random DES key (ECB mode) to simulate an exposed ciphertext:

```python 
from Crypto.Cipher import DES
import os

plaintext = b"sup3rshy"  # 8 bytes
key = os.urandom(8)      # Random DES key (8 bytes)
cipher = DES.new(key, DES.MODE_ECB)
ciphertext = cipher.encrypt(plaintext)

print("plaintext (hex):", plaintext.hex())
print("ciphertext (hex):", ciphertext.hex())
print("secret key (hex):", key.hex())  # Only for lab verification
```


Assumption: the attacker knows plaintext and ciphertext but not the secret key.

## 3. CPU-Based Brute-Force Script

A multiprocessing Python script (bruteforce_des_mp.py) performs exhaustive key search across a configurable keyspace. For lab reproducibility, runs typically use a reduced keyspace (e.g., 2^16, 2^20, or 2^24) before scaling up.

Run (example):

python experiments/exp_des_bruteforce/bruteforce_des_mp.py


Key parameters to configure in the script:

MODE or LIMIT (determines demo keyspace size)

number of worker processes (cpu_count() used by default)

plaintext/ciphertext inputs (load from data/ if preferred)

logging output file (CSV or JSON for metrics)

## 4. Hashcat-Based GPU Attack

Hashcat supports DES known-plaintext attacks using mode 14000 (DES-ECB with known plaintext). The input format is a colon separated pair:

```<plaintext_hex>:<ciphertext_hex>```


Example hash file (hashes.txt):

```7375703372736879:5df07a2f8b26ec65```


(Left is plaintext hex for "sup3rshy", right is ciphertext hex.)

Basic brute-force command (mask attack):

```hashcat -m 14000 hashes.txt -a 3 ?b?b?b?b?b?b?b?b --hex-charset```


-m 14000 selects DES known-plaintext mode.

-a 3 is mask (brute-force) attack.

?b means binary byte (full 0x00–0xFF) when used with --hex-charset (try 8 bytes = full 64-bit keyspace).

Notes:

For ASCII-only keys you can use ?a/?l/?d masks to reduce search space.

Use hashcat -b to benchmark GPU performance before a long run.

Use --session and --restore to support long jobs and checkpointing.

## 5. Logging and Timing

Record the following metrics for every experiment run:

Time-to-key-recovery (wall-clock)

Keys attempted (total)

Throughput (keys/sec, CPU vs GPU)

System metrics: CPU/GPU utilization, memory, temperature (if available)

Run metadata: Hashcat version, GPU model, Python version, script parameters, exact plaintext/ciphertext

## 6. Practical guidance & safety

Start small: use a reduced keyspace (e.g., 2^16, 2^20) to validate scripts and measurement pipelines.

Scaling: move to GPU Hashcat for larger spaces; split keyspace across multiple nodes when appropriate.

Ethics: run only on test vectors and isolated lab systems. Do not target third-party systems.

Parity bits: DES has parity bits (one parity bit per byte). PyCryptodome accepts 8-byte keys directly; if you want to enforce parity you must set parity bits when generating trial keys.

Reproducibility: record every parameter and the exact random seed used (if any). Publish scripts and logs in experiments/exp_des_bruteforce/ and data/ for reproducibility.

## 7. Expected outcomes (what to report)

A working CPU demo that recovers keys in small keyspaces (time and throughput reported).

A Hashcat GPU run showing keys/sec and estimated time for full 2^56 search (and cost estimates if run on cloud GPU instances).

An analysis paragraph concluding the practical infeasibility/cost of brute-forcing DES in production and recommending migration to AES/AEAD.
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
