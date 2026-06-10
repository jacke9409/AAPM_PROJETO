from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from app.database import criar_tabelas
from app.routers import (
    auth_router,
    admin_router,
    categoria_router,
    produto_router,
    venda_router,
    publico_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    yield


app = FastAPI(title="AAPM PDV", lifespan=lifespan)

# ── Arquivos estáticos ────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router.router)
app.include_router(admin_router.router)
app.include_router(categoria_router.router)
app.include_router(produto_router.router)
app.include_router(venda_router.router)
app.include_router(publico_router.router)