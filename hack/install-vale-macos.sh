#!/usr/bin/env bash
# Install Vale and sync Gardener style rules on macOS
set -euo pipefail

if command -v vale >/dev/null 2>&1; then
  echo "Vale is already installed: $(vale --version)"
else
  if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew is required to install Vale. Install it from https://brew.sh and re-run this script."
    exit 1
  fi
  echo "Installing Vale via Homebrew..."
  brew install vale
fi

echo "Syncing Gardener Vale style rules..."
vale sync

echo ""
echo "Vale is ready. Run 'make vale' to lint your changes."
echo "For editor integration, install the Vale VS Code extension:"
echo "  https://marketplace.visualstudio.com/items?itemName=ChrisChinchilla.vale-vscode"
