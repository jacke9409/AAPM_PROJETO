from fastapi import APIRouter, Request, Response, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os

from app.database import get_db
from app.models import Usuario, RoleEnum

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ── Configurações JWT ─────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "troque-essa-chave-no-env")
ALGORITHM = "HS256"
EXPIRE_HOURS = 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ── Helpers ───────────────────────────────────────────────────────────────────
def verificar_senha(senha_plana: str, hash_: str) -> bool:
    return pwd_context.verify(senha_plana, hash_)


def gerar_hash(senha: str) -> str:
    return pwd_context.hash(senha)


def criar_token(usuario: Usuario) -> str:
    payload = {
        "id": usuario.id,
        "email": usuario.email,
        "role": usuario.role.value,
        "exp": datetime.utcnow() + timedelta(hours=EXPIRE_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_usuario_logado(request: Request, db: Session = Depends(get_db)) -> Usuario:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Não autenticado")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = db.query(Usuario).filter(Usuario.id == payload["id"]).first()
        if not usuario:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


def exigir_admin(usuario: Usuario = Depends(get_usuario_logado)) -> Usuario:
    if usuario.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return usuario


# ── Rotas ─────────────────────────────────────────────────────────────────────
@router.get("/login", response_class=HTMLResponse)
def tela_login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
def fazer_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "erro": "E-mail ou senha incorretos"},
            status_code=400,
        )

    token = criar_token(usuario)
    response = RedirectResponse(url="/admin/dashboard", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=EXPIRE_HOURS * 3600,
        samesite="lax",
    )
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response