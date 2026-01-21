#!/bin/bash
# ============================================================
# DeepFake MIA - Lanceur Ubuntu
# Lance l'application et ouvre le navigateur en plein écran
# ============================================================

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
APP_URL="http://localhost:5000"

# S'assurer que DISPLAY est défini (important pour lancement depuis .desktop)
export DISPLAY="${DISPLAY:-:0}"

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     🎭  DeepFake MIA - Lanceur                               ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Vérifier que le venv existe
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}❌ Environnement virtuel non trouvé: $VENV_DIR${NC}"
    notify-send "DeepFake MIA" "Environnement virtuel non trouvé" --icon=error 2>/dev/null
    exit 1
fi

# Activer l'environnement virtuel
echo -e "${YELLOW}🔄 Activation de l'environnement virtuel...${NC}"
source "$VENV_DIR/bin/activate"

# Vérifier que Flask est installé
if ! python -c "import flask" 2>/dev/null; then
    echo -e "${RED}❌ Flask n'est pas installé${NC}"
    notify-send "DeepFake MIA" "Flask n'est pas installé" --icon=error 2>/dev/null
    exit 1
fi

# Fonction pour attendre que le serveur soit prêt
wait_for_server() {
    echo -e "${YELLOW}⏳ Attente du serveur...${NC}"
    for i in {1..30}; do
        if curl -s "$APP_URL" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Serveur prêt!${NC}"
            return 0
        fi
        sleep 0.5
    done
    echo -e "${RED}❌ Timeout: le serveur n'a pas démarré${NC}"
    return 1
}

# Fonction pour ouvrir le navigateur en plein écran
open_browser() {
    echo -e "${GREEN}🌐 Ouverture du navigateur en plein écran...${NC}"
    
    # Essayer différents navigateurs (kiosk mode = plein écran sans barre)
    if command -v firefox &> /dev/null; then
        firefox --kiosk "$APP_URL" &
        echo -e "${GREEN}✅ Firefox ouvert en mode kiosk${NC}"
    elif command -v chromium-browser &> /dev/null; then
        chromium-browser --kiosk --disable-infobars --disable-session-crashed-bubble "$APP_URL" &
        echo -e "${GREEN}✅ Chromium ouvert en mode kiosk${NC}"
    elif command -v google-chrome &> /dev/null; then
        google-chrome --kiosk --disable-infobars --disable-session-crashed-bubble "$APP_URL" &
        echo -e "${GREEN}✅ Chrome ouvert en mode kiosk${NC}"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "$APP_URL" &
        echo -e "${YELLOW}⚠️  Navigateur ouvert - Appuyez sur F11 pour le plein écran${NC}"
    else
        echo -e "${YELLOW}⚠️  Aucun navigateur trouvé. Ouvrez manuellement: $APP_URL${NC}"
        notify-send "DeepFake MIA" "Ouvrez $APP_URL dans votre navigateur" 2>/dev/null
    fi
}

# Fonction de nettoyage à la fermeture
cleanup() {
    echo -e "\n${YELLOW}🛑 Arrêt de l'application...${NC}"
    # Tuer les processus enfants
    jobs -p | xargs -r kill 2>/dev/null
    exit 0
}

# Capturer Ctrl+C et fermeture
trap cleanup SIGINT SIGTERM EXIT

# Aller dans le répertoire du projet
cd "$SCRIPT_DIR"

# Lancer l'application Flask en arrière-plan
echo -e "${GREEN}🚀 Démarrage de DeepFake MIA...${NC}"
python app.py &
FLASK_PID=$!

# Attendre que le serveur soit prêt puis ouvrir le navigateur
if wait_for_server; then
    open_browser
fi

# Notification de démarrage
notify-send "DeepFake MIA" "Application démarrée sur $APP_URL" --icon=applications-multimedia 2>/dev/null

# Attendre que Flask se termine
wait $FLASK_PID
