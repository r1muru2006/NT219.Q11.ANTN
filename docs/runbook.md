# Padding Oracle PoC (lab)

## Requirements
- Python >= 3.8
- pwntools
- pycryptodome


## Files
- vuln.py : vulnerable TCP server (port 1337)
- attack_padding_oracle.py : attacker script (targets port 1337)
- patched_server_aead.py : AEAD TCP server (port 7331)


## Run vulnerable lab (Docker)
1. Move to the directory containing docker: `cd docker`
2. Building docker for the first time: `docker-compose up -d --build`
(if not the first time: `docker-compose up -d`)
3. Move to the folder containing the attack script: `cd ../scripts`
4. Run attack scripts: `python attack_padding_oracle.py` (Padding Oracle Attack)

## Stop lab
- Just to stop: `docker-compose stop`
- Stop and uninstall the container: `docker-compose down`
- Reconnect the docker again: `docker-compose up -d`

# GCM Nonce Reuse PoC (lab)

## Requirements
- Python >= 3.8
- pwntools
- pycryptodome


## Files
- vuln.py : vulnerable TCP server (port 21337)
- attack_gcm_nonce_reuse.py : attacker script (targets port 21337)


## Run vulnerable lab (Docker)
1. Move to the directory containing docker: `cd docker`
2. Building docker for the first time: `docker-compose up -d --build`
(if not the first time: `docker-compose up -d`)
3. Move to the folder containing the attack script: `cd ../scripts`
4. Run attack scripts: `python attack_gcm_nonce_reuse.py` (GCM Forbidden Attack)

## Stop lab
- Just to stop: `docker-compose stop`
- Stop and uninstall the container: `docker-compose down`
- Reconnect the docker again: `docker-compose up -d`