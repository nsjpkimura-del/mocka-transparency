$ErrorActionPreference = "Stop"
$root = Resolve-Path "$PSScriptRoot\.."
$sample = Join-Path $root "sample03"
$f = Join-Path $sample "decision_new.json"

Write-Host "1) Verify before tamper"
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root "scripts\verify_sample03.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "2) Tamper decision_new.json (append [TAMPERED])"
$j = Get-Content -Raw -Encoding UTF8 $f | ConvertFrom-Json
$j.note = ($j.note + " [TAMPERED]")
($j | ConvertTo-Json -Depth 20) | Set-Content -Encoding UTF8 $f

Write-Host "Tampered file: $f"
Write-Host ""
Write-Host "3) Verify after tamper (must FAIL)"
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root "scripts\verify_sample03.ps1")
exit $LASTEXITCODE
