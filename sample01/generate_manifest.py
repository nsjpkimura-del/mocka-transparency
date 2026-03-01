import hashlib
import json
from datetime import datetime, timezone

INPUT_FILE = "decision_log.json"
OUTPUT_FILE = "manifest.json"

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    sha = sha256_file(INPUT_FILE)
    manifest = {
        "schema": "mocka.transparency.manifest.v1",
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "file": INPUT_FILE,
        "sha256": sha,
        "signed_by": "Outfield-Test-2026",
        "signature_file": "signature.bin"
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("OK manifest.json generated")
    print("sha256:", sha)

if __name__ == "__main__":
    main()
