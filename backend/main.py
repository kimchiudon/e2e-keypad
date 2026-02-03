from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.keypad import router as keypad_router
from utils.image_utils import load_image_base64  # 너의 함수명에 맞추기

REQUIRED_ASSETS = [str(i) for i in range(10)] + ["EMPTY"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 전 검사
    for name in REQUIRED_ASSETS:
        load_image_base64(name)  # lru_cache면 동시에 워밍업도 됨
    yield
    # 종료 시 정리할 게 있으면 여기

app = FastAPI(title="E2E Keypad Backend Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(keypad_router)
