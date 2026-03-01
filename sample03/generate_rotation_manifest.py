import hashlib
import json
from datetime import datetime, timezone

FILES = ["decision_old.json", "decision_new.json"]
OUT = "rotation_manifest.json"

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    entries = [{"file": fn, "sha256": sha256_file(fn)} for fn in FILES]

    manifest = {
        "schema": "mocka.transparency.sample03.rotation_manifest.v1",
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rotation": {
            "from_key": "Outfield-Test-2026",
            "to_key": "Outfield-Test-2028",
            "reason": "key compromise simulation"
        },
        "entries": entries,
        "signature_old": "sig_old.bin",
        "signature_new": "sig_new.bin"
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("OK rotation_manifest.json generated")

if __name__ == "__main__":
    main()
