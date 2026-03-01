$ErrorActionPreference = "Stop"

$root = Resolve-Path "$PSScriptRoot\.."
$sample = Join-Path $root "sample02"

$pyExe = Resolve-Path (Join-Path $root ".venv\Scripts\python.exe")
$verifyPy = Resolve-Path (Join-Path $root "tools\verify_sig.py")

$manifestPath = Join-Path $sample "chain_manifest.json"
$sigPath = Join-Path $sample "chain_signature.bin"
$pubKeyPath = Resolve-Path (Join-Path $root "public_keys\Verifier-Test-2026_public.pem")

if (!(Test-Path $manifestPath)) { throw "missing chain_manifest.json" }
if (!(Test-Path $sigPath)) { throw "missing chain_signature.bin" }

# 1) verify signature over sha256(manifest)
& $pyExe $verifyPy $pubKeyPath $manifestPath $sigPath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 2) verify chain integrity
$manifest = Get-Content -Raw -Encoding UTF8 $manifestPath | ConvertFrom-Json

function Sha256File([string]$p) {
  (Get-FileHash -Algorithm SHA256 -Path $p).Hash.ToLower()
}

$prev = ("0" * 64)
foreach ($e in $manifest.entries) {
  $filePath = Join-Path $sample $e.file
  if (!(Test-Path $filePath)) { throw "missing file: $($e.file)" }

  $h = (Sha256File $filePath)
  if ($h -ne $e.sha256.ToLower()) {
    Write-Host "FAIL: file sha256 mismatch: $($e.file)"
    Write-Host "expected: $($e.sha256)"
    Write-Host "actual  : $h"
    exit 21
  }

  $chain = [System.BitConverter]::ToString(
    (New-Object System.Security.Cryptography.SHA256Managed).ComputeHash(
      [System.Text.Encoding]::ASCII.GetBytes($prev + $h)
    )
  ).Replace("-", "").ToLower()

  if ($chain -ne $e.chain_hash.ToLower()) {
    Write-Host "FAIL: chain hash mismatch: $($e.file)"
    Write-Host "expected: $($e.chain_hash)"
    Write-Host "actual  : $chain"
    exit 22
  }

  $prev = $chain
}

if ($prev -ne $manifest.final_chain_hash.ToLower()) {
  Write-Host "FAIL: final_chain_hash mismatch"
  Write-Host "expected: $($manifest.final_chain_hash)"
  Write-Host "actual  : $prev"
  exit 23
}

Write-Host "PASS: Sample02 verified"
exit 0
