import time
from typing import Dict, Any, Optional

# ✅ 반드시 모듈 레벨(함수 밖)이어야 함: 요청 끝나도 유지됨
_sessions_db: Dict[str, Dict[str, Any]] = {}

def save_session(session_id: str, mapping: Dict[str, str], expires_at: float) -> None:
    _sessions_db[session_id] = {
        "expires_at": expires_at,
        "mapping": mapping,
        "created_at": time.time(),
    }

def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    cleanup_expired_sessions()
    return _sessions_db.get(session_id)

def cleanup_expired_sessions() -> None:
    now = time.time()
    expired = [sid for sid, data in _sessions_db.items() if data["expires_at"] <= now]
    for sid in expired:
        del _sessions_db[sid]
