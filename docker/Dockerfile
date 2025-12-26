FROM python:3.10-alpine

# Install socat
RUN apk add --no-cache --update socat

WORKDIR /chal

# --- Setup Lab 1 (Padding Oracle) ---
RUN mkdir -p /chal/oracle
COPY experiments/exp_padding_oracle/requirements.txt /chal/oracle/
COPY experiments/exp_padding_oracle/vuln.py /chal/oracle/vuln.py

# --- Setup Lab 2 (GCM Nonce) ---
RUN mkdir -p /chal/gcm
COPY experiments/exp_gcm_nonce_reuse/requirements.txt /chal/gcm/
COPY experiments/exp_gcm_nonce_reuse/vuln.py /chal/gcm/vuln.py

# --- Install Requirements ---
# We install dependencies for both labs
RUN pip3 install -r /chal/oracle/requirements.txt
RUN pip3 install -r /chal/gcm/requirements.txt