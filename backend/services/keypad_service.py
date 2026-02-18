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

    mapping: Dict[str, str] = {}
    layout: List[KeypadCell] = []

    salt = os.urnadom(16)
    inner_value = hashlib.sha256(salt).hexdigest()

    for pos, inner_value in enumerate():
        for i in range (DIGITS): 
            pos = DIGITS[i],
            mapping[pos] = inner_value
            
            try:
                img_b64 = load_image_base64(pos)
                
            except FileNotFoundError as e:
                raise HTTPException(status_code=400, detail=str(e))

    random.shuffle(mapping)  
    
    layout.append(
            KeypadCell(
                inner_value=inner_value,
                image=img_b64,
                is_blank=(inner_value is None),
            )
        )


    save_session(session_id=session_id, mapping=mapping, expires_at=expires_at)

    return KeypadInitResponse(
        session_id=session_id,
        expires_at=expires_at,
        layout=layout,
    )
