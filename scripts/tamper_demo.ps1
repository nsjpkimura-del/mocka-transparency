$ErrorActionPreference = "Stop"

$root   = Resolve-Path "$PSScriptRoot\.."
$sample = Join-Path $root "sample01"
$decision = Join-Path $sample "decision_log.json"

Write-Host "1) Verify before tamper"
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root "scripts\verify_one.ps1")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "2) Tamper decision_log.json (append [TAMPERED] to reason)"

$json = Get-Content -Raw -Encoding UTF8 $decision | ConvertFrom-Json
$json.reason = ($json.reason + " [TAMPERED]")
($json | ConvertTo-Json -Depth 20) | Set-Content -Encoding UTF8 $decision

Write-Host "Tampered file: $decision"
Write-Host ""
Write-Host "3) Verify after tamper (must FAIL)"
powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root "scripts\verify_one.ps1")
exit $LASTEXITCODE
