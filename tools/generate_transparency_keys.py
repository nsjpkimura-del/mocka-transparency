from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta, timezone
import hashlib
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KEYS_DIR = os.path.join(ROOT, "keys")
PUB_DIR = os.path.join(ROOT, "public_keys")

COMMENT = "Transparency v2 only"
VALID_DAYS = 730  # 2 years

def ensure_dirs():
    os.makedirs(KEYS_DIR, exist_ok=True)
    os.makedirs(PUB_DIR, exist_ok=True)

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def write_file(path: str, data: bytes):
    with open(path, "wb") as f:
        f.write(data)

def generate(name: str):
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()

    priv_pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    pub_pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    priv_path = os.path.join(KEYS_DIR, f"{name}_private.pem")
    pub_path = os.path.join(PUB_DIR, f"{name}_public.pem")

    write_file(priv_path, priv_pem)
    write_file(pub_path, pub_pem)

    fp = sha256_hex(pub_pem)

    now = datetime.now(timezone.utc)
    exp = (now + timedelta(days=VALID_DAYS)).date().isoformat()

    return {
        "name": name,
        "comment": COMMENT,
        "expires_utc_date": exp,
        "sha256_fingerprint": fp,
        "public_key_path": os.path.relpath(pub_path, ROOT),
        "private_key_path": os.path.relpath(priv_path, ROOT),
    }

def main():
    ensure_dirs()

    keys = [
        generate("Verifier-Test-2026"),
        generate("Outfield-Test-2026"),
    ]

    print("Generated keys (public keys are commit-safe, private keys are NOT).")
    for k in keys:
        print("-" * 60)
        print("Name:", k["name"])
        print("Comment:", k["comment"])
        print("Expires(UTC date):", k["expires_utc_date"])
        print("SHA256 Fingerprint:", k["sha256_fingerprint"])
        print("Public:", k["public_key_path"])
        print("Private:", k["private_key_path"])

if __name__ == "__main__":
    main()