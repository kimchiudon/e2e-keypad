from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    SESSION_TTL_SECONDS: int = 300   # 5분
    TOKEN_BYTES: int = 16            # 16 bytes -> 32 hex chars
    SESSION_ID_BYTES: int = 16       # 16 bytes -> 32 hex chars
    ASSETS_DIR: str = "assets"       # backend/assets

settings = Settings()
