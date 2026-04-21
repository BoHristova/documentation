#!/usr/bin/env bash
# Install Vale and sync Gardener style rules on Linux
set -euo pipefail

VALE_VERSION="3.14.1"
INSTALL_DIR="$HOME/.local/bin"

if command -v vale >/dev/null 2>&1; then
  echo "Vale is already installed: $(vale --version)"
else
  echo "Installing Vale ${VALE_VERSION} for Linux..."
  mkdir -p "$INSTALL_DIR"
  curl -sL "https://github.com/errata-ai/vale/releases/download/v${VALE_VERSION}/vale_${VALE_VERSION}_Linux_64-bit.tar.gz" \
    | tar -xz -C "$INSTALL_DIR" vale
  chmod +x "$INSTALL_DIR/vale"

  if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    echo ""
    echo "Add the following to your ~/.bashrc or ~/.zshrc to make vale available:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "Then run: source ~/.bashrc (or ~/.zshrc)"
  fi
fi

echo "Syncing Gardener Vale style rules..."
vale sync

echo ""
echo "Vale is ready. Run 'make vale' to lint your changes."
echo "For editor integration, install the Vale VS Code extension:"
echo "  https://marketplace.visualstudio.com/items?itemName=ChrisChinchilla.vale-vscode"
