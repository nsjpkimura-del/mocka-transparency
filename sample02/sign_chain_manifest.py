from cryptography.hazmat.primitives import serialization
import hashlib
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SAMPLE = os.path.join(ROOT, "sample02")

PRIVKEY = os.path.join(ROOT, "keys", "Verifier-Test-2026_private.pem")
MANIFEST = os.path.join(SAMPLE, "chain_manifest.json")
SIG = os.path.join(SAMPLE, "chain_signature.bin")

def main():
    with open(PRIVKEY, "rb") as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)

    with open(MANIFEST, "rb") as f:
        b = f.read()

    digest = hashlib.sha256(b).digest()
    sig = priv.sign(digest)

    with open(SIG, "wb") as f:
        f.write(sig)

    print("OK chain_signature.bin written")

if __name__ == "__main__":
    main()
