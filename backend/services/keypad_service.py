import time
import random
import secrets
from typing import Dict, List

from fastapi import HTTPException
from core.config import settings
from models.keypad_models import KeypadInitResponse, KeypadCell
from services.session_service import save_session, cleanup_expired_sessions
from utils.image_utils import load_image_base64
import os
import hashlib

def _new_session_id() -> str:
    return secrets.token_hex(settings.SESSION_ID_BYTES)


def create_keypad_session() -> KeypadInitResponse:

    cleanup_expired_sessions()


    session_id = _new_session_id()
    expires_at = time.time() + settings.SESSION_TTL_SECONDS


    DIGITS = [0,1,2,3,4,5,6,7,8,9,None,None]

    mapping = {}
    layout = []
    skirt = ["0","0","0","0","0","0","0","0","0","0","0","0"]
    i=0
    real_value = 0

    for pos, inner_value in enumerate(skirt):
        pos = DIGITS[i]

        if pos != None:
            salt = os.urandom(16)
            real_value = hashlib.sha256(salt).hexdigest()
            inner_value = str (real_value)
            mapping[pos] = inner_value
            
            try:
                img_b64 = load_image_base64(pos)
            
            except FileNotFoundError as e:
                raise HTTPException(status_code=400, detail=str(e))
                
            save_session(session_id=session_id, mapping=mapping, expires_at=expires_at)

        else:
            img_b64 = load_image_base64("EMPTY")
            inner_value = "0"
            save_session(session_id=session_id, mapping={}, expires_at=expires_at)
        
        i = i + 1

    layout.append(
        KeypadCell(
            inner_value=inner_value,
            image=img_b64,
            is_blank=(pos is None),
        )
    )
    
    return KeypadInitResponse(
        session_id=session_id,
        expires_at=expires_at,
        layout=layout,
    )
