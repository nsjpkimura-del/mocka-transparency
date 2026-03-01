# MoCKA Transparency v2

Japanese version: README.ja.md

---

## 3-Minute Transparency Demo (Sample01)

This demo lets you experience tamper detection.

Flow:

1. Verify the sealed state (PASS)
2. Tamper with the file
3. Verification fails (FAIL)
4. Restore and verify again (PASS)

---

### 1. Clone

git clone https://github.com/nsjpkimura-del/mocka-transparency.git
cd mocka-transparency

---

### 2. Verify (should PASS)

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_one.ps1

Expected output:
PASS: Sample01 verified

---

### 3. Run tamper demo (should FAIL)

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\tamper_demo.ps1

Expected output:
FAIL: decision_log.json sha256 mismatch

---

### 4. Restore (PASS again)

git restore .\sample01\decision_log.json
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_one.ps1

---

What this demonstrates:

- Sealed logs cannot be silently modified
- Tampering is immediately detected
- Verification uses only public keys
- Recovery is deterministic via Git