param(
  [string]$SampleDir = "$(Resolve-Path "$PSScriptRoot\..\sample01")"
)

$ErrorActionPreference = "Stop"

function Get-Sha256Hex([string]$Path) {
  $h = Get-FileHash -Algorithm SHA256 -Path $Path
  return $h.Hash.ToLower()
}

function Read-Json([string]$Path) {
  return Get-Content -Raw -Encoding UTF8 $Path | ConvertFrom-Json
}

$pyExe = Resolve-Path "$PSScriptRoot\..\.venv\Scripts\python.exe"
$verifyPy = Resolve-Path "$PSScriptRoot\..\tools\verify_sig.py"

Write-Host "Python: $pyExe"
Write-Host "SampleDir: $SampleDir"

$decisionPath = Join-Path $SampleDir "decision_log.json"
$manifestPath = Join-Path $SampleDir "manifest.json"
$sigPath      = Join-Path $SampleDir "signature.bin"
$pubKeyPath   = Resolve-Path "$PSScriptRoot\..\public_keys\Outfield-Test-2026_public.pem"

if (!(Test-Path $decisionPath)) { throw "missing decision_log.json" }
if (!(Test-Path $manifestPath)) { throw "missing manifest.json" }
if (!(Test-Path $sigPath))      { throw "missing signature.bin" }

$manifest = Read-Json $manifestPath

$expected = $manifest.sha256.ToLower()
$actual = (Get-Sha256Hex $decisionPath)

if ($expected -ne $actual) {
  Write-Host "FAIL: decision_log.json sha256 mismatch"
  Write-Host "expected: $expected"
  Write-Host "actual  : $actual"
  exit 2
}

Write-Host "OK: decision_log.json sha256 matches manifest"

& $pyExe $verifyPy $pubKeyPath $manifestPath $sigPath
$code = $LASTEXITCODE
if ($code -ne 0) { exit $code }

Write-Host "PASS: Sample01 verified"
exit 0
