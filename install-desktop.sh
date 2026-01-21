#!/bin/bash
# ============================================================
# Installation du raccourci DeepFake MIA dans le menu Ubuntu
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_FILE="$SCRIPT_DIR/DeepFake-MIA.desktop"
INSTALL_DIR="$HOME/.local/share/applications"

echo "🎭 Installation du raccourci DeepFake MIA..."

# Créer le répertoire si nécessaire
mkdir -p "$INSTALL_DIR"

# Mettre à jour les chemins dans le fichier .desktop
cat > "$INSTALL_DIR/DeepFake-MIA.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=DeepFake MIA
Comment=Face Swap en temps réel - La Maison de l'IA
Icon=$SCRIPT_DIR/static/images/MIA_Blanc.png
Exec=$SCRIPT_DIR/launch.sh
Path=$SCRIPT_DIR
Terminal=false
Categories=Graphics;Video;
Keywords=deepfake;faceswap;ia;ai;
StartupNotify=true
EOF

# Rendre exécutable
chmod +x "$INSTALL_DIR/DeepFake-MIA.desktop"

# Mettre à jour la base de données des applications
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$INSTALL_DIR" 2>/dev/null
fi

echo "✅ Raccourci installé!"
echo "   Vous pouvez maintenant lancer 'DeepFake MIA' depuis le menu Applications"
echo ""
echo "📌 Ou créer un raccourci sur le Bureau:"
echo "   cp $INSTALL_DIR/DeepFake-MIA.desktop ~/Bureau/"
