from fastapi import APIRouter
from models.keypad_models import KeypadInitResponse, KeypadSubmitRequest
from services.keypad_service import create_keypad_session, user_input

router = APIRouter(prefix="/keypad", tags=["keypad"])

@router.get("/init", response_model=KeypadInitResponse)
def init_keypad():
    # ✅ 라우터는 얇게: 서비스만 호출
    return create_keypad_session()

@router.post("/submit")
def input_keypad(payload: KeypadSubmitRequest):
    return user_input(payload)