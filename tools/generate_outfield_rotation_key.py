from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta, timezone
import hashlib
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KEYS = os.path.join(ROOT, "keys")
PUB = os.path.join(ROOT, "public_keys")

NAME = "Outfield-Test-2028"
COMMENT = "Transparency v2 only"
VALID_DAYS = 730

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def write(path: str, data: bytes):
    with open(path, "wb") as f:
        f.write(data)

def main():
    os.makedirs(KEYS, exist_ok=True)
    os.makedirs(PUB, exist_ok=True)

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

    priv_path = os.path.join(KEYS, f"{NAME}_private.pem")
    pub_path = os.path.join(PUB, f"{NAME}_public.pem")

    write(priv_path, priv_pem)
    write(pub_path, pub_pem)

    fp = sha256_hex(pub_pem)
    exp = (datetime.now(timezone.utc) + timedelta(days=VALID_DAYS)).date().isoformat()

    print(NAME)
    print("Comment:", COMMENT)
    print("Expires(UTC date):", exp)
    print("SHA256 Fingerprint:", fp)
    print("Public:", os.path.relpath(pub_path, ROOT))
    print("Private:", os.path.relpath(priv_path, ROOT))

if __name__ == "__main__":
    main()
