import time
import random
import secrets
from typing import Dict, List

from fastapi import HTTPException
from core.config import settings
from models.keypad_models import KeypadInitResponse, KeypadCell
from services.session_service import save_session, cleanup_expired_sessions
from utils.image_utils import load_image_base64

DIGITS = [str(i) for i in range(10)]
BLANK = "EMPTY"

def _new_session_id() -> str:
    return secrets.token_hex(settings.SESSION_ID_BYTES)

def _new_token() -> str:
    return secrets.token_hex(settings.TOKEN_BYTES)

def create_keypad_session() -> KeypadInitResponse:
    """
    - session_id 생성
    - 12칸(0~9 + EMPTY 2개) 셔플
    - 각 칸 token 생성
    - mapping(token -> digit/EMPTY) 생성 후 서버 내부 저장
    - 프론트로는 layout(토큰/이미지/pos/is_blank)만 반환
    """
    # 1) 만료 세션 정리 (lazy cleanup)
    cleanup_expired_sessions()

    # 2) session_id / expires_at
    session_id = _new_session_id()
    expires_at = time.time() + settings.SESSION_TTL_SECONDS

    # 3) 12칸 값 만들고 셔플
    values = DIGITS + [BLANK, BLANK]
    random.shuffle(values)

    mapping: Dict[str, str] = {}
    layout: List[KeypadCell] = []

    # 4) token/mapping/layout 생성
    for pos, value in enumerate(values):
        token = _new_token()
        mapping[token] = value

        try:
            img_b64 = load_image_base64(value)
        except FileNotFoundError as e:
            # 과제/디버깅 시 원인 바로 알게 400으로
            raise HTTPException(status_code=400, detail=str(e))

        layout.append(
            KeypadCell(
                pos=pos,
                token=token,
                image=img_b64,
                is_blank=(value == BLANK),
            )
        )

    # 5) 세션 저장 (mapping은 프론트에 절대 안 줌)
    save_session(session_id=session_id, mapping=mapping, expires_at=expires_at)

    return KeypadInitResponse(
        session_id=session_id,
        expires_at=expires_at,
        layout=layout,
    )
