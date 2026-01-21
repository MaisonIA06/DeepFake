#!/usr/bin/env python3
"""
DeepFake MIA - Application Web
Face Swap en temps réel par MIA - La Maison de l'IA

Usage:
    python app.py

Puis ouvrez http://localhost:5000 dans votre navigateur.
"""

import os
import sys
from flask import Flask, render_template, jsonify, request, send_from_directory

# Configuration
from config import (
    BASE_DIR, STATIC_DIR, TEMPLATES_DIR, FACES_DIR,
    PLAYERS_LEFT, PLAYERS_RIGHT, DEFAULT_OPTIONS, FLASK_CONFIG
)

# ============================================================
# Initialisation Flask
# ============================================================

app = Flask(
    __name__,
    static_folder=STATIC_DIR,
    template_folder=TEMPLATES_DIR
)
app.config['SECRET_KEY'] = FLASK_CONFIG['SECRET_KEY']

# ============================================================
# État de l'application
# ============================================================

app_state = {
    "selected_player": None,
    "is_running": False,
    "options": DEFAULT_OPTIONS.copy()
}

# ============================================================
# Routes principales
# ============================================================

@app.route('/')
def index():
    """Page principale de l'application"""
    return render_template(
        'index.html',
        players_left=PLAYERS_LEFT,
        players_right=PLAYERS_RIGHT
    )

@app.route('/static/faces/<filename>')
def serve_face(filename):
    """Servir les images de visages"""
    return send_from_directory(FACES_DIR, filename)

@app.route('/static/images/<filename>')
def serve_image(filename):
    """Servir les images (logo, fond)"""
    return send_from_directory(os.path.join(STATIC_DIR, 'images'), filename)

@app.route('/static/css/<filename>')
def serve_css(filename):
    """Servir les fichiers CSS"""
    return send_from_directory(os.path.join(STATIC_DIR, 'css'), filename)

# ============================================================
# API Endpoints
# ============================================================

@app.route('/api/select_face', methods=['POST'])
def api_select_face():
    """Sélectionner un visage pour le deepfake"""
    data = request.get_json()
    player_id = data.get('player')
    
    if not player_id:
        return jsonify({"success": False, "error": "Player ID requis"}), 400
    
    app_state["selected_player"] = player_id
    
    # TODO: Intégrer avec le module core
    # from core import globals
    # globals.source_path = os.path.join(FACES_DIR, f"{player_id}.png")
    
    return jsonify({
        "success": True,
        "player": player_id,
        "message": f"Visage {player_id} sélectionné"
    })

@app.route('/api/start', methods=['POST'])
def api_start():
    """Démarrer le deepfake"""
    data = request.get_json()
    
    if not app_state["selected_player"]:
        return jsonify({"success": False, "error": "Aucun visage sélectionné"}), 400
    
    app_state["is_running"] = True
    if data.get('options'):
        app_state["options"].update(data['options'])
    
    # TODO: Démarrer le traitement deepfake
    # from core.processors.frame.face_swapper import process_frame
    
    return jsonify({
        "success": True,
        "message": "DeepFake démarré",
        "state": app_state
    })

@app.route('/api/stop', methods=['POST'])
def api_stop():
    """Arrêter le deepfake"""
    app_state["is_running"] = False
    
    # TODO: Arrêter le traitement deepfake
    
    return jsonify({
        "success": True,
        "message": "DeepFake arrêté"
    })

@app.route('/api/option', methods=['POST'])
def api_option():
    """Mettre à jour une option"""
    data = request.get_json()
    option = data.get('option')
    value = data.get('value')
    
    if option not in app_state["options"]:
        return jsonify({"success": False, "error": f"Option inconnue: {option}"}), 400
    
    app_state["options"][option] = value
    
    # TODO: Mettre à jour les options dans le module core
    # from core import globals
    # setattr(globals, option, value)
    
    return jsonify({
        "success": True,
        "option": option,
        "value": value
    })

@app.route('/api/status')
def api_status():
    """Obtenir le statut actuel"""
    return jsonify(app_state)

@app.route('/api/players')
def api_players():
    """Obtenir la liste des joueurs"""
    return jsonify({
        "left": PLAYERS_LEFT,
        "right": PLAYERS_RIGHT
    })

# ============================================================
# Fonctions utilitaires
# ============================================================

def get_available_cameras():
    """Obtenir la liste des caméras disponibles"""
    cameras = []
    try:
        import cv2
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append({"id": str(i), "name": f"Caméra {i + 1}"})
                cap.release()
    except ImportError:
        cameras = [{"id": "0", "name": "Caméra par défaut"}]
    return cameras

# ============================================================
# Point d'entrée
# ============================================================

def main():
    """Point d'entrée principal"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     🎭  DeepFake MIA - La Maison de l'IA                     ║
    ║                                                              ║
    ║     Interface Web pour Face Swap en temps réel               ║
    ║                                                              ║
    ║     📍 Ouvrez votre navigateur :                             ║
    ║        http://localhost:5000                                 ║
    ║                                                              ║
    ║     ⏹  Appuyez sur Ctrl+C pour arrêter                       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(
        host=FLASK_CONFIG['HOST'],
        port=FLASK_CONFIG['PORT'],
        debug=FLASK_CONFIG['DEBUG'],
        threaded=True
    )

if __name__ == '__main__':
    main()
