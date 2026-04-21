# Install Vale and sync Gardener style rules on Windows
# Run in PowerShell as Administrator if using Chocolatey

$ErrorActionPreference = "Stop"
$ValeVersion = "3.14.1"

if (Get-Command vale -ErrorAction SilentlyContinue) {
    Write-Host "Vale is already installed: $(vale --version)"
} elseif (Get-Command choco -ErrorAction SilentlyContinue) {
    Write-Host "Installing Vale via Chocolatey..."
    choco install vale -y
} else {
    Write-Host "Chocolatey not found. Downloading Vale binary..."
    $InstallDir = "$env:LOCALAPPDATA\vale"
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    $Url = "https://github.com/errata-ai/vale/releases/download/v$ValeVersion/vale_${ValeVersion}_Windows_64-bit.zip"
    $ZipPath = "$env:TEMP\vale.zip"
    Invoke-WebRequest -Uri $Url -OutFile $ZipPath
    Expand-Archive -Path $ZipPath -DestinationPath $InstallDir -Force
    Remove-Item $ZipPath

    $CurrentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($CurrentPath -notlike "*$InstallDir*") {
        [Environment]::SetEnvironmentVariable("PATH", "$CurrentPath;$InstallDir", "User")
        Write-Host "Added $InstallDir to your PATH. Restart your terminal to apply."
    }
}

Write-Host "Syncing Gardener Vale style rules..."
vale sync

Write-Host ""
Write-Host "Vale is ready. Run 'make vale' to lint your changes."
Write-Host "For editor integration, install the Vale VS Code extension:"
Write-Host "  https://marketplace.visualstudio.com/items?itemName=ChrisChinchilla.vale-vscode"
