from typing import Any, List
import cv2
import threading
import gfpgan
import os

import core.globals
from core.face_analyser import get_one_face
from core.typing import Frame, Face
import platform
import torch

FACE_ENHANCER = None
THREAD_SEMAPHORE = threading.Semaphore()
THREAD_LOCK = threading.Lock()
NAME = "DLC.FACE-ENHANCER"

abs_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(abs_dir))), "models"
)


def get_face_enhancer() -> Any:
    global FACE_ENHANCER

    with THREAD_LOCK:
        if FACE_ENHANCER is None:
            model_path = os.path.join(models_dir, "GFPGANv1.4.pth")
            
            match platform.system():
                case "Darwin":  # Mac OS
                    if torch.backends.mps.is_available():
                        mps_device = torch.device("mps")
                        FACE_ENHANCER = gfpgan.GFPGANer(model_path=model_path, upscale=1, device=mps_device)
                    else:
                        FACE_ENHANCER = gfpgan.GFPGANer(model_path=model_path, upscale=1)
                case _:  # Other OS
                    FACE_ENHANCER = gfpgan.GFPGANer(model_path=model_path, upscale=1)

    return FACE_ENHANCER


def enhance_face(temp_frame: Frame) -> Frame:
    with THREAD_SEMAPHORE:
        _, _, temp_frame = get_face_enhancer().enhance(temp_frame, paste_back=True)
    return temp_frame


def process_frame(source_face: Face, temp_frame: Frame) -> Frame:
    target_face = get_one_face(temp_frame)
    if target_face:
        temp_frame = enhance_face(temp_frame)
    return temp_frame


def process_frame_v2(temp_frame: Frame) -> Frame:
    target_face = get_one_face(temp_frame)
    if target_face:
        temp_frame = enhance_face(temp_frame)
    return temp_frame
