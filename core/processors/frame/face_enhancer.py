from typing import Any, List
import cv2
import threading
import os
import logging

import core.globals
from core.face_analyser import get_one_face
from core.typing import Frame, Face

# Tenter d'importer gfpgan (peut échouer avec certaines versions de torchvision)
GFPGAN_AVAILABLE = False
try:
    import gfpgan
    import platform
    import torch
    GFPGAN_AVAILABLE = True
except ImportError as e:
    logging.warning(f"GFPGAN non disponible: {e}")

FACE_ENHANCER = None
FACE_ENHANCER_FAILED = False
THREAD_SEMAPHORE = threading.Semaphore()
THREAD_LOCK = threading.Lock()
NAME = "DLC.FACE-ENHANCER"

abs_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(abs_dir))), "models"
)


def get_face_enhancer() -> Any:
    global FACE_ENHANCER, FACE_ENHANCER_FAILED

    if not GFPGAN_AVAILABLE or FACE_ENHANCER_FAILED:
        return None

    with THREAD_LOCK:
        if FACE_ENHANCER is None:
            try:
                model_path = os.path.join(models_dir, "GFPGANv1.4.pth")
                
                if not os.path.exists(model_path):
                    logging.warning(f"Modèle GFPGAN non trouvé: {model_path}")
                    FACE_ENHANCER_FAILED = True
                    return None
                
                match platform.system():
                    case "Darwin":  # Mac OS
                        if torch.backends.mps.is_available():
                            mps_device = torch.device("mps")
                            FACE_ENHANCER = gfpgan.GFPGANer(model_path=model_path, upscale=1, device=mps_device)
                        else:
                            FACE_ENHANCER = gfpgan.GFPGANer(model_path=model_path, upscale=1)
                    case _:  # Other OS
                        FACE_ENHANCER = gfpgan.GFPGANer(model_path=model_path, upscale=1)
                        
                logging.info("GFPGAN Face Enhancer chargé avec succès")
            except Exception as e:
                logging.warning(f"Impossible de charger GFPGAN: {e}")
                FACE_ENHANCER_FAILED = True
                return None

    return FACE_ENHANCER


def enhance_face(temp_frame: Frame) -> Frame:
    enhancer = get_face_enhancer()
    if enhancer is None:
        return temp_frame
    
    try:
        with THREAD_SEMAPHORE:
            _, _, temp_frame = enhancer.enhance(temp_frame, paste_back=True)
    except Exception as e:
        logging.debug(f"Erreur lors de l'enhancement: {e}")
    return temp_frame


def process_frame(source_face: Face, temp_frame: Frame) -> Frame:
    if not is_available():
        return temp_frame
    target_face = get_one_face(temp_frame)
    if target_face:
        temp_frame = enhance_face(temp_frame)
    return temp_frame


def process_frame_v2(temp_frame: Frame) -> Frame:
    if not is_available():
        return temp_frame
    target_face = get_one_face(temp_frame)
    if target_face:
        temp_frame = enhance_face(temp_frame)
    return temp_frame


def is_available() -> bool:
    """Vérifie si le Face Enhancer est disponible"""
    return GFPGAN_AVAILABLE and not FACE_ENHANCER_FAILED
