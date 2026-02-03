from fastapi import APIRouter
from models.keypad_models import KeypadInitResponse
from services.keypad_service import create_keypad_session

router = APIRouter(prefix="/keypad", tags=["keypad"])

@router.get("/init", response_model=KeypadInitResponse)
def init_keypad():
    # ✅ 라우터는 얇게: 서비스만 호출
    return create_keypad_session()
