# 🎭 DeepFake MIA

**Face Swap en temps réel** - Interface Web moderne développée par **MIA - La Maison de l'IA**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Description

DeepFake MIA est une application web permettant d'effectuer du **face swap en temps réel** via webcam. L'interface moderne et intuitive permet de sélectionner facilement un visage source parmi une galerie de joueurs et d'appliquer le deepfake instantanément.

### ✨ Fonctionnalités

- 🎥 **Face Swap temps réel** via webcam
- 👤 **12 visages pré-configurés** (joueurs)
- 🎨 **Interface web moderne** (responsive)
- ⚙️ **Options avancées** :
  - Mouth Mask (préserve la bouche originale)
  - Face Enhancer (amélioration qualité GFPGAN)
  - Many Faces (multi-visages)
  - Affichage FPS

---

## 🏗️ Structure du Projet

```
DeepFake-MIA/
├── app.py                    # 🚀 Point d'entrée principal
├── config.py                 # ⚙️ Configuration globale
├── requirements.txt          # 📦 Dépendances Python
├── README.md                 # 📖 Documentation
├── LICENSE                   # 📄 Licence
│
├── core/                     # 🧠 Logique métier
│   ├── __init__.py
│   ├── globals.py            # Variables globales
│   ├── face_analyser.py      # Détection de visage
│   ├── video_capture.py      # Capture vidéo
│   ├── utilities.py          # Fonctions utilitaires
│   └── processors/           # Processeurs de frame
│       └── frame/
│           ├── face_swapper.py
│           └── face_enhancer.py
│
├── models/                   # 🤖 Modèles IA
│   ├── inswapper_128_fp16.onnx
│   ├── GFPGANv1.4.pth
│   └── (autres modèles)
│
├── gfpgan/                   # 🎨 Poids GFPGAN
│   └── weights/
│       ├── detection_Resnet50_Final.pth
│       └── parsing_parsenet.pth
│
├── static/                   # 🎨 Assets web
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   ├── MIA_Assets12.jpg  # Fond terracotta
│   │   └── MIA_Blanc.png     # Logo MIA
│   └── faces/
│       └── *.png             # Visages des joueurs
│
└── templates/                # 📄 Templates HTML
    └── index.html
```

---

## 🚀 Installation

### Prérequis

- **Python 3.10+**
- **CUDA** (recommandé pour GPU NVIDIA)
- **Webcam**

### Étapes

1. **Cloner le projet**
```bash
git clone https://github.com/MaisonIA06/DeepFake.git
cd DeepFake
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Télécharger les modèles** (si non inclus)

Placez les fichiers suivants dans le dossier `models/` :
- `inswapper_128_fp16.onnx` - [Télécharger](https://https://huggingface.co/ninjawick/webui-faceswap-unlocked/blob/main/inswapper_128_fp16.onnx)
- `GFPGANv1.4.pth` - [Télécharger](https://https://huggingface.co/gmk123/GFPGAN/blob/main/GFPGANv1.4.pth)

---

## 🎮 Utilisation

### Lancer l'application

```bash
python app.py
```

### Accéder à l'interface

Ouvrez votre navigateur à l'adresse :
```
http://localhost:5000
```

### Comment utiliser

1. **Sélectionnez un visage** dans les panels gauche ou droit
2. **Cliquez sur "Démarrer DeepFake"**
3. **Autorisez l'accès** à votre webcam
4. **Profitez** du face swap en temps réel !

---

## ⚙️ Options

| Option | Description | Impact Performance |
|--------|-------------|-------------------|
| **Mouth Mask** | Préserve la bouche originale | ✅ Léger |
| **Face Enhancer** | Améliore la qualité (GFPGAN) | ⚠️ Lourd |
| **Many Faces** | Swap tous les visages détectés | ⚠️ Lourd |
| **Show FPS** | Affiche les images/seconde | ✅ Aucun |

---

## 🎨 Personnalisation

### Ajouter de nouveaux visages

1. Ajoutez l'image PNG dans `static/faces/`
2. Modifiez `config.py` pour ajouter le joueur :

```python
PLAYERS = [
    # ... joueurs existants ...
    {"id": "NOUVEAU", "name": "Nouveau Joueur", "position": "left"},
]
```

### Modifier le thème

Éditez `static/css/style.css` pour personnaliser :
- Couleurs (variables CSS)
- Polices
- Espacements

---

## 🔧 Configuration

Modifiez `config.py` pour ajuster :

```python
# Serveur Web
FLASK_CONFIG = {
    "HOST": "0.0.0.0",    # Interface réseau
    "PORT": 5000,         # Port
    "DEBUG": True,        # Mode debug
}

# Performance
EXECUTION_PROVIDERS = ['CUDAExecutionProvider', 'CPUExecutionProvider']
MAX_MEMORY = 8  # GB
```

---

## 🐛 Dépannage

### Erreur CUDA non trouvé
```bash
pip install onnxruntime  # Version CPU
```

### Webcam non détectée
- Vérifiez les permissions du navigateur
- Essayez un autre navigateur (Chrome recommandé)

### Performance faible
- Désactivez "Face Enhancer"
- Réduisez la résolution de la webcam
- Utilisez un GPU NVIDIA avec CUDA

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🏢 Crédits

Développé par **MIA - La Maison de l'IA**

Basé sur le projet open-source [Deep-Live-Cam](https://github.com/hacksider/Deep-Live-Cam)

---

## ⚠️ Avertissement

Cette application est destinée à un usage **éducatif et ludique uniquement**. 

L'utilisation de deepfakes doit se faire :
- Avec le **consentement** des personnes concernées
- Dans le **respect de la vie privée**
- Sans intention de **nuire ou tromper**

Les créateurs de cette application déclinent toute responsabilité en cas d'utilisation abusive.
