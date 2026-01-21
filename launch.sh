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
    echo -e "${YELLOW}Créez-le avec: python -m venv venv && pip install -r requirements.txt${NC}"
    exit 1
fi

# Activer l'environnement virtuel
echo -e "${YELLOW}🔄 Activation de l'environnement virtuel...${NC}"
source "$VENV_DIR/bin/activate"

# Vérifier que Flask est installé
if ! python -c "import flask" 2>/dev/null; then
    echo -e "${RED}❌ Flask n'est pas installé${NC}"
    echo -e "${YELLOW}Installez les dépendances: pip install -r requirements.txt${NC}"
    exit 1
fi

# Fonction pour ouvrir le navigateur en plein écran
open_browser() {
    sleep 3  # Attendre que le serveur démarre
    
    echo -e "${GREEN}🌐 Ouverture du navigateur en plein écran...${NC}"
    
    # Essayer différents navigateurs (kiosk mode = plein écran sans barre)
    if command -v chromium-browser &> /dev/null; then
        chromium-browser --kiosk --disable-infobars --disable-session-crashed-bubble "$APP_URL" &
    elif command -v google-chrome &> /dev/null; then
        google-chrome --kiosk --disable-infobars --disable-session-crashed-bubble "$APP_URL" &
    elif command -v firefox &> /dev/null; then
        firefox --kiosk "$APP_URL" &
    elif command -v xdg-open &> /dev/null; then
        xdg-open "$APP_URL" &
        echo -e "${YELLOW}⚠️  Appuyez sur F11 pour le plein écran${NC}"
    else
        echo -e "${YELLOW}⚠️  Aucun navigateur trouvé. Ouvrez manuellement: $APP_URL${NC}"
    fi
}

# Fonction de nettoyage à la fermeture
cleanup() {
    echo -e "\n${YELLOW}🛑 Arrêt de l'application...${NC}"
    # Tuer les processus enfants
    pkill -P $$
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT SIGTERM

# Lancer le navigateur en arrière-plan
open_browser &

# Lancer l'application Flask
echo -e "${GREEN}🚀 Démarrage de DeepFake MIA...${NC}"
cd "$SCRIPT_DIR"
python app.py

# Nettoyage
cleanup
