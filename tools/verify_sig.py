from cryptography.hazmat.primitives import serialization
import hashlib
import sys

pub_path, manifest_path, sig_path = sys.argv[1], sys.argv[2], sys.argv[3]

with open(pub_path, "rb") as f:
    pub = serialization.load_pem_public_key(f.read())

with open(manifest_path, "rb") as f:
    manifest_bytes = f.read()

with open(sig_path, "rb") as f:
    sig = f.read()

digest = hashlib.sha256(manifest_bytes).digest()

try:
    pub.verify(sig, digest)
    print("OK: signature verified")
    sys.exit(0)
except Exception as e:
    print("FAIL: signature verify error:", str(e))
    sys.exit(3)
