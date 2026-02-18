from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.keypad import router as keypad_router
from utils.image_utils import load_image_base64  

REQUIRED_ASSETS = [str(i) for i in range(10)] + ["EMPTY"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    for name in REQUIRED_ASSETS:
        load_image_base64(name)  
    
    yield
   

app = FastAPI(title="E2E Keypad Backend Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(keypad_router)
