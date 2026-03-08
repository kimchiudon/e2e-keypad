from fastapi import APIRouter, HTTPException
from models.keypad_models import KeypadInitResponse, KeypadSubmitRequest
from services.keypad_service import create_keypad_session
from services.session_service import get_session
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

router = APIRouter(prefix="/keypad", tags=["keypad"])


@router.get("/init", response_model=KeypadInitResponse)
def init_keypad():
    return create_keypad_session()


@router.post("/submit")
def input_keypad(payload: KeypadSubmitRequest):
    try:
        with open("private_key.pem", "rb") as f:
            private_key = RSA.import_key(f.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"private key load failed: {str(e)}")

    try:
        cipher = PKCS1_v1_5.new(private_key)
        decrypted = cipher.decrypt(base64.b64decode(payload.encrypted_data), None)

        if decrypted is None:
            raise ValueError("decryption returned None")

        decrypted_text = decrypted.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"decrypt failed: {str(e)}")

    session_data = get_session(payload.session_id)

    print("\n=== 프론트에서 받은 암호문 ===")
    print(payload.encrypted_data)

    print("\n=== 복호화 결과 ===")
    print(decrypted_text)

    print("\n=== 해당 세션 해시테이블 ===")
    if session_data:
        print(session_data["mapping"])
    else:
        print("session not found")

    return {
        "result": "success",
        "decrypted_text": decrypted_text,
    }