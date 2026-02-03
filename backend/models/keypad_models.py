from pydantic import BaseModel
from typing import List

class KeypadCell(BaseModel):
    pos: int
    token: str
    image: str          # data:image/png;base64,...
    is_blank: bool

class KeypadInitResponse(BaseModel):
    session_id: str
    expires_at: float
    layout: List[KeypadCell]
