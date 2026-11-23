# Vektra Laws installer for Windows (PowerShell 5.1 or 7+).
#
#   iex (irm https://vektraindustries.com/laws/install.ps1)
#
# Read it first (recommended):
#   irm https://vektraindustries.com/laws/install.ps1 -OutFile install.ps1; notepad install.ps1
#   powershell -ExecutionPolicy Bypass -File install.ps1
#
# Same steps as install.sh: check Python 3.10+ and git, download into %LOCALAPPDATA%\vektra-laws\src,
# make a private venv, verify the Laws against LAWS.lock, add the vektra-laws command, run setup.
# Env: VEKTRA_LAWS_HOME, VEKTRA_LAWS_REF, VEKTRA_LAWS_REPO, VEKTRA_LAWS_NO_SETUP=1
$ErrorActionPreference = "Stop"

# Steward key fingerprints (SHA-256 of each raw Ed25519 public key), comma-separated: main key, then
# recovery key. Same values as VERIFYING.md and vektraindustries.com. Empty until the first signed release.
$PinnedKeys = ""
$Trusted = if ($env:VEKTRA_LAWS_TRUSTED_KEYS) { $env:VEKTRA_LAWS_TRUSTED_KEYS } else { $PinnedKeys }

$Repo   = if ($env:VEKTRA_LAWS_REPO) { $env:VEKTRA_LAWS_REPO } else { "https://github.com/Vektra-Industries/vektra-laws.git" }
$Api    = "https://api.github.com/repos/Vektra-Industries/vektra-laws/releases/latest"
$VLHome = if ($env:VEKTRA_LAWS_HOME) { $env:VEKTRA_LAWS_HOME } else { Join-Path $env:LOCALAPPDATA "vektra-laws" }
$Ref    = $env:VEKTRA_LAWS_REF

function Say($m)  { Write-Host "==> $m" -ForegroundColor Yellow }
function Fail($m) { Write-Host "error: $m" -ForegroundColor Red; exit 1 }

Write-Host "`nVektra Laws" -ForegroundColor White
Write-Host "A safety core for AI, agents and robots. Humans stay in command.`n"

# 1. Requirements
$Py = $null
foreach ($c in @(@("py", "-3"), @("python"), @("python3"))) {
    $exe = Get-Command $c[0] -ErrorAction SilentlyContinue
    if (-not $exe) { continue }
    $args0 = @($c | Select-Object -Skip 1)
    & $exe.Source @args0 -c "import sys, venv, ensurepip; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>$null
    if ($LASTEXITCODE -eq 0) { $Py = @($exe.Source) + $args0; break }
}
if (-not $Py) { Fail "Python 3.10 or newer is needed. Install it with: winget install Python.Python.3.12" }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Fail "git is needed. Install it with: winget install Git.Git" }
Say "Python and git found"

# 2. Download
if (-not $Ref) {
    try { $Ref = (Invoke-RestMethod -Uri $Api -UseBasicParsing).tag_name } catch { $Ref = $null }
}
if (-not $Ref) { $Ref = "main" }
$Src = Join-Path $VLHome "src"
New-Item -ItemType Directory -Force -Path $VLHome | Out-Null
if (Test-Path (Join-Path $Src ".git")) {
    Say "Updating Vektra Laws in $Src to $Ref"
    git -C $Src fetch --quiet --tags origin
    git -C $Src checkout --quiet --force $Ref 2>$null
    if ($LASTEXITCODE -ne 0) { git -C $Src checkout --quiet --force "origin/$Ref" }
} else {
    Say "Downloading Vektra Laws ($Ref) into $Src"
    if (Test-Path $Src) { Remove-Item -Recurse -Force $Src }
    git clone --quiet --depth 1 --branch $Ref $Repo $Src
    if ($LASTEXITCODE -ne 0) { Fail "Download failed. Check your connection, or that release $Ref exists." }
}

# 3. Private Python environment
$Venv = Join-Path $VLHome "venv"
$VPy  = Join-Path $Venv "Scripts\python.exe"
if (-not (Test-Path $VPy)) {
    Say "Making a private Python environment"
    $pyArgs = @($Py | Select-Object -Skip 1) + @("-m", "venv", $Venv)
    & $Py[0] @pyArgs
}
& $VPy -m pip install --quiet --disable-pip-version-check --upgrade pip
& $VPy -m pip install --quiet --disable-pip-version-check -r (Join-Path $Src "requirements.txt")

# 4. Verify the Laws
Say "Checking the Laws against LAWS.lock"
$env:PYTHONPATH = Join-Path $Src "core"
$env:VEKTRA_LAWS_TRUSTED_KEYS = $Trusted
$vArgs = @("-m", "vektra_laws_core", "verify")
foreach ($f in ($Trusted -split ",")) { if ($f.Trim()) { $vArgs += @("--expect-key", $f.Trim()) } }
& $VPy @vArgs
if ($LASTEXITCODE -ne 0) { Fail "The Laws did not verify. Nothing was added to your PATH. Please report this to security@vektraindustries.com." }

# 5. The command
$Bin = Join-Path $VLHome "bin"
New-Item -ItemType Directory -Force -Path $Bin | Out-Null
$Launcher = Join-Path $Bin "vektra-laws.cmd"
@"
@echo off
rem vektra-laws launcher, written by the Vektra Laws installer (VEKTRA_LAWS_HOME).
set "VEKTRA_LAWS_HOME=$VLHome"
set "VEKTRA_LAWS_BIN=$Bin"
set "VEKTRA_LAWS_TRUSTED_KEYS=$Trusted"
set "PYTHONPATH=$Src\core;%PYTHONPATH%"
"$VPy" -m vektra_laws_core %*
"@ | Set-Content -Encoding ASCII $Launcher
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not ($userPath -split ";" | Where-Object { $_ -eq $Bin })) {
    [Environment]::SetEnvironmentVariable("Path", "$Bin;$userPath", "User")
}
$env:Path = "$Bin;$env:Path"
Say "Installed the vektra-laws command at $Launcher"

# 6. Setup wizard
if (-not $env:VEKTRA_LAWS_NO_SETUP -and [Environment]::UserInteractive) {
    Write-Host ""
    & $Launcher setup
} else {
    Write-Host "`nRun 'vektra-laws setup' in your project folder to set it up."
}
Write-Host "`nDone. Open a new terminal, then try: vektra-laws doctor"
