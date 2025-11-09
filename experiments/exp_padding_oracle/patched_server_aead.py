# patched_server_aead.py -- use AES-GCM
from flask import Flask, request, abort
from Crypto.Cipher import AES
import binascii
import os

app = Flask(__name__)
KEY = os.urandom(16)


@app.route('/decrypt', methods=['POST'])
def decrypt_endpoint():
    j = request.get_json(force=True)
    if not j or 'ct' not in j:
        abort(400)
    try:
        raw = binascii.unhexlify(j['ct'])
        # format: nonce(12) || ct || tag(16)
        if len(raw) < 12 + 16:
            abort(400)
        nonce = raw[:12]
        tag = raw[-16:]
        ct = raw[12:-16]
    except Exception:
        abort(400)
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=nonce)
    try:
        pt = cipher.decrypt_and_verify(ct, tag)
    except ValueError:
        # generic failure; no padding oracles
        abort(403)
    return {"ok": True, "plaintext_hex": binascii.hexlify(pt).decode()}


if __name__ == '__main__':
    app.run(port=7331, debug=False)