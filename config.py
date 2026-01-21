"""
DeepFake MIA - Configuration
Paramètres globaux de l'application
"""

import os

# ============================================================
# Chemins
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
FACES_DIR = os.path.join(STATIC_DIR, 'faces')

# Modèles IA
INSWAPPER_MODEL = os.path.join(MODELS_DIR, 'inswapper_128_fp16.onnx')
GFPGAN_MODEL = os.path.join(MODELS_DIR, 'GFPGANv1.4.pth')
GFPGAN_WEIGHTS_DIR = os.path.join(BASE_DIR, 'gfpgan', 'weights')

# ============================================================
# Joueurs / Visages disponibles
# ============================================================

PLAYERS = [
    {"id": "AH-KONG", "name": "Ah-Kong", "position": "left"},
    {"id": "BARNES", "name": "Barnes", "position": "left"},
    {"id": "BRIGGS", "name": "Briggs", "position": "left"},
    {"id": "CASTELNAU", "name": "Castelnau", "position": "left"},
    {"id": "DULSKI", "name": "Dulski", "position": "left"},
    {"id": "KEEMINK", "name": "Keemink", "position": "left"},
    {"id": "KICIAK", "name": "Kiciak", "position": "right"},
    {"id": "LIBERMAN", "name": "Liberman", "position": "right"},
    {"id": "MCHENRY", "name": "McHenry", "position": "right"},
    {"id": "NACK-MINYEM", "name": "Nack-Minyem", "position": "right"},
    {"id": "NAMBOUE", "name": "Namboue", "position": "right"},
    {"id": "RAJOHARIVELO", "name": "Rajoharivelo", "position": "right"},
]

PLAYERS_LEFT = [p for p in PLAYERS if p["position"] == "left"]
PLAYERS_RIGHT = [p for p in PLAYERS if p["position"] == "right"]

# ============================================================
# Options par défaut
# ============================================================

DEFAULT_OPTIONS = {
    "mouth_mask": False,
    "face_enhancer": False,
    "show_fps": False,
    "many_faces": False,
}

# ============================================================
# Serveur Web
# ============================================================

FLASK_CONFIG = {
    "SECRET_KEY": "deepfake-mia-2025",
    "DEBUG": True,
    "HOST": "0.0.0.0",
    "PORT": 5000,
}

# ============================================================
# Exécution
# ============================================================

EXECUTION_PROVIDERS = ['CUDAExecutionProvider', 'CPUExecutionProvider']
EXECUTION_THREADS = 8
MAX_MEMORY = 8  # GB
