import time
import random
import secrets
from typing import Dict, List

from fastapi import HTTPException, Request
from core.config import settings
from models.keypad_models import KeypadInitResponse, KeypadCell, KeypadSubmitRequest
from services.session_service import save_session, cleanup_expired_sessions
from utils.image_utils import load_image_base64
import os
import hashlib

import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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
    real_value = 0
    i = 0

    for pos, inner_value in enumerate(skirt):

        pos = DIGITS[i]

        if pos is not None:
            salt = os.urandom(16)
            real_value = secrets.token_hex(8)
            inner_value = str (real_value)
            mapping[pos] = inner_value
            k = str(pos)

            try:
                img_b64 = load_image_base64(k)
            
            except FileNotFoundError as e:
                raise HTTPException(status_code=400, detail=str(e))
                

        else:
            img_b64 = load_image_base64("EMPTY")
            salt = os.urandom(16)
            real_value = secrets.token_hex(8)
            inner_value = str (real_value)

        
        i = i + 1
 
        layout.append(
            KeypadCell(
                inner_value=inner_value,
                image=img_b64,
                is_blank=(pos is None),
                )
        )

    save_session(session_id=session_id, mapping=mapping, expires_at=expires_at)


    random.shuffle(layout)

    return KeypadInitResponse(
        session_id=session_id,
        expires_at=expires_at,
        layout=layout,
    )

def user_input(payload: KeypadSubmitRequest) -> dict:
    session_id = payload.session_id
    tokens = payload.tokens
    
    print(f"[submit] session_id={session_id}")
    print(f"[submit] tokens={tokens}")

    return {
        "result": "ok",
        "session_id": session_id,
        "tokens_count": len(tokens),
    }
