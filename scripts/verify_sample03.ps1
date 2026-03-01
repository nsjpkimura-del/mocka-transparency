$ErrorActionPreference = "Stop"

$root = Resolve-Path "$PSScriptRoot\.."
$sample = Join-Path $root "sample03"

$pyExe = Resolve-Path (Join-Path $root ".venv\Scripts\python.exe")
$verifyPy = Resolve-Path (Join-Path $root "tools\verify_sig.py")

$manifestPath = Join-Path $sample "rotation_manifest.json"
if (!(Test-Path $manifestPath)) { throw "missing rotation_manifest.json" }

$manifest = Get-Content -Raw -Encoding UTF8 $manifestPath | ConvertFrom-Json

function Sha256File([string]$p) {
  (Get-FileHash -Algorithm SHA256 -Path $p).Hash.ToLower()
}

foreach ($e in $manifest.entries) {
  $fp = Join-Path $sample $e.file
  if (!(Test-Path $fp)) { throw "missing file: $($e.file)" }
  $h = (Sha256File $fp)
  if ($h -ne $e.sha256.ToLower()) {
    Write-Host "FAIL: file sha256 mismatch: $($e.file)"
    exit 31
  }
}
Write-Host "OK: files sha256 match manifest"

$oldPub = Resolve-Path (Join-Path $root "public_keys\Outfield-Test-2026_public.pem")
$oldSig = Join-Path $sample $manifest.signature_old
& $pyExe $verifyPy $oldPub $manifestPath $oldSig
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "OK: old signature verified"

$newPub = Resolve-Path (Join-Path $root "public_keys\Outfield-Test-2028_public.pem")
$newSig = Join-Path $sample $manifest.signature_new
& $pyExe $verifyPy $newPub $manifestPath $newSig
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "OK: new signature verified"

Write-Host "PASS: Sample03 verified"
exit 0
