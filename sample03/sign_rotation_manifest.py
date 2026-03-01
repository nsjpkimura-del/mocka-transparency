from cryptography.hazmat.primitives import serialization
import hashlib
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SAMPLE = os.path.join(ROOT, "sample03")

MANIFEST = os.path.join(SAMPLE, "rotation_manifest.json")

OLD_PRIV = os.path.join(ROOT, "keys", "Outfield-Test-2026_private.pem")
NEW_PRIV = os.path.join(ROOT, "keys", "Outfield-Test-2028_private.pem")

SIG_OLD = os.path.join(SAMPLE, "sig_old.bin")
SIG_NEW = os.path.join(SAMPLE, "sig_new.bin")

def sign(priv_path: str, out_path: str, digest: bytes):
    with open(priv_path, "rb") as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)
    sig = priv.sign(digest)
    with open(out_path, "wb") as f:
        f.write(sig)

def main():
    with open(MANIFEST, "rb") as f:
        b = f.read()
    digest = hashlib.sha256(b).digest()

    sign(OLD_PRIV, SIG_OLD, digest)
    sign(NEW_PRIV, SIG_NEW, digest)

    print("OK sig_old.bin and sig_new.bin written")

if __name__ == "__main__":
    main()
