from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import hashlib
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PRIVKEY_PATH = os.path.join(ROOT, "keys", "Outfield-Test-2026_private.pem")
MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "manifest.json")
SIG_PATH = os.path.join(os.path.dirname(__file__), "signature.bin")

def sha256_bytes(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def main():
    with open(PRIVKEY_PATH, "rb") as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)

    with open(MANIFEST_PATH, "rb") as f:
        manifest_bytes = f.read()

    digest = sha256_bytes(manifest_bytes)
    sig = priv.sign(digest)

    with open(SIG_PATH, "wb") as f:
        f.write(sig)

    print("OK signature.bin written")

if __name__ == "__main__":
    main()
