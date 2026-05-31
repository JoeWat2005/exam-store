#!/bin/bash
# vlab-setup.sh — make JupyterLab open .md files in Preview mode by default.
# Run once on vLab. Persists across sessions (lives in ~/.jupyter/).
#
# Usage on vLab:
#   bash vlab-setup.sh
#   ... then refresh JupyterLab tab (Ctrl+R)

set -e

SETTINGS_DIR="$HOME/.jupyter/lab/user-settings/@jupyterlab/docmanager-extension"
SETTINGS_FILE="$SETTINGS_DIR/plugin.jupyterlab-settings"

mkdir -p "$SETTINGS_DIR"

cat > "$SETTINGS_FILE" << 'EOF'
{
    "defaultViewers": {
        "markdown": "Markdown Preview"
    }
}
EOF

echo "Written: $SETTINGS_FILE"
echo ""
echo "Done. Now REFRESH the JupyterLab browser tab (Ctrl+R)."
echo "After refresh, every .md file opens in Preview mode automatically."
echo ""
echo "To revert later:"
echo "  rm '$SETTINGS_FILE'"
