#!/bin/bash

echo "Checking for Python..."
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python 3 to continue."
    exit 1
fi

echo "Checking for 'uv'..."
if ! command -v uv &> /dev/null; then
    echo "'uv' is not installed. Installing 'uv'..."
    curl -Ls https://astral.sh/uv/install.sh | bash
    export PATH="$HOME/.cargo/bin:$PATH"
fi

UV_PATH="$(which uv)"

if [ -z "$UV_PATH" ]; then
    echo "Failed to install or locate 'uv'. Please install it manually from https://github.com/astral-sh/uv"
    exit 1
fi

echo "'uv' is installed at $UV_PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "Creating virtual environment..."
"$UV_PATH" venv "$VENV_DIR"

echo "Installing dependencies from pyproject.toml..."
cd "$SCRIPT_DIR"
"$UV_PATH" pip install .

echo "Running Python config generator..."
"$VENV_DIR/bin/python" "$SCRIPT_DIR/setup_config.py" "$SCRIPT_DIR" "$UV_PATH"

CONFIG_PATH="$SCRIPT_DIR/config.json"

if [ ! -f "$CONFIG_PATH" ]; then
    echo "Config file was not created. Exiting."
    exit 1
fi

echo "🚀 Starting MCP..."
"$UV_PATH" run python "$(jq -r '.mcpServers.filegen.args[2]' "$CONFIG_PATH")"
