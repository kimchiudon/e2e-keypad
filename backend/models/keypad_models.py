from pydantic import BaseModel
from typing import List
from typing import Optional

class KeypadCell(BaseModel):
    inner_value: str
    image: str          # data:image/png;base64,...
    is_blank: bool

class KeypadInitResponse(BaseModel):
    session_id: str
    expires_at: float
    layout: List[KeypadCell]

class KeypadSubmitRequest(BaseModel):
    session_id: str
    encrypted_data: str