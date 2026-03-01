import hashlib
import json
from datetime import datetime, timezone

FILES = ["decision_001.json", "decision_002.json", "decision_003.json"]
OUT = "chain_manifest.json"

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    entries = []
    prev = "0" * 64
    for fn in FILES:
        h = sha256_file(fn)
        chain_hash = hashlib.sha256((prev + h).encode("ascii")).hexdigest()
        entries.append({
            "file": fn,
            "sha256": h,
            "prev_chain_hash": prev,
            "chain_hash": chain_hash
        })
        prev = chain_hash

    manifest = {
        "schema": "mocka.transparency.sample02.chain_manifest.v1",
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "signed_by": "Verifier-Test-2026",
        "entries": entries,
        "final_chain_hash": prev,
        "signature_file": "chain_signature.bin"
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("OK chain_manifest.json generated")
    print("final_chain_hash:", prev)

if __name__ == "__main__":
    main()
