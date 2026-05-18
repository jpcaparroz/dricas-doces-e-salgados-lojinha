from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import init_db
from routers.products import router as products_router
from routers.orders import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server starting...")
    yield
    print("Server shutting down...")

app = FastAPI(
    title="Dricas Doces e Salgados Lojinha API",
    description="Backend da lojinha",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(orders_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Dricas Doces e Salgados API rodando!"
    }