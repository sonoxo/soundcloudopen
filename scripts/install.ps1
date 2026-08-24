$ErrorActionPreference = "Stop"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw "Python 3.10+ is required. Install Python and rerun this script."
}

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements
  } elseif (Get-Command choco -ErrorAction SilentlyContinue) {
    choco install ffmpeg -y
  } else {
    throw "FFmpeg is required. Install it with winget/chocolatey, then rerun."
  }
}

python -m pip install --upgrade pip
python -m pip install .
Write-Host "Installed. Run: soundcloudopen --check"
