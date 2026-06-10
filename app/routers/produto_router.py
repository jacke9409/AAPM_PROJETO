import os
import shutil
import uuid

from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Produto, Categoria, Fornecedor, Usuario
from app.routers.auth_router import get_usuario_logado, exigir_admin

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "app/static/assets/produtos"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def salvar_imagem(arquivo: UploadFile) -> str | None:
    """Salva o arquivo em static/assets/produtos e devolve o caminho relativo."""
    if not arquivo or not arquivo.filename:
        return None
    ext = os.path.splitext(arquivo.filename)[1].lower()
    nome_unico = f"{uuid.uuid4().hex}{ext}"
    destino = os.path.join(UPLOAD_DIR, nome_unico)
    with open(destino, "wb") as f:
        shutil.copyfileobj(arquivo.file, f)
    return f"/static/assets/produtos/{nome_unico}"


# ── Listagem ──────────────────────────────────────────────────────────────────
@router.get("/produtos", response_class=HTMLResponse)
def listar_produtos(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_logado),
):
    produtos = db.query(Produto).order_by(Produto.nome).all()
    return templates.TemplateResponse(
        "admin/produtos_lista.html",
        {"request": request, "usuario": usuario, "produtos": produtos},
    )


# ── Detalhes ──────────────────────────────────────────────────────────────────
@router.get("/produtos/{id}", response_class=HTMLResponse)
def detalhe_produto(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_logado),
):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return templates.TemplateResponse(
        "admin/produtos_detalhe.html",
        {"request": request, "usuario": usuario, "produto": produto},
    )


# ── Criar ─────────────────────────────────────────────────────────────────────
@router.get("/produtos/novo/form", response_class=HTMLResponse)
def form_novo_produto(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    categorias = db.query(Categoria).order_by(Categoria.nome).all()
    fornecedores = db.query(Fornecedor).order_by(Fornecedor.nome).all()

    # Lista imagens já existentes em assets para o seletor
    imagens_existentes = []
    if os.path.isdir(UPLOAD_DIR):
        imagens_existentes = [
            f"/static/assets/produtos/{f}"
            for f in os.listdir(UPLOAD_DIR)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif"))
        ]

    return templates.TemplateResponse(
        "admin/produtos_form.html",
        {
            "request": request,
            "usuario": usuario,
            "editando": None,
            "categorias": categorias,
            "fornecedores": fornecedores,
            "imagens_existentes": imagens_existentes,
        },
    )


@router.post("/produtos/novo/form")
def criar_produto(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(""),
    preco: float = Form(...),
    tamanho: str = Form(""),
    estoque: int = Form(0),
    categoria_id: int = Form(None),
    fornecedor_id: int = Form(None),
    imagem_existente: str = Form(""),   # caminho de imagem já salva
    imagem: UploadFile = File(None),    # upload novo
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    # Prioridade: upload novo > imagem existente escolhida
    caminho_imagem = salvar_imagem(imagem) or imagem_existente or None

    produto = Produto(
        nome=nome,
        descricao=descricao,
        preco=preco,
        tamanho=tamanho,
        estoque=estoque,
        disponivel=estoque > 0,
        imagem=caminho_imagem,
        categoria_id=categoria_id,
        fornecedor_id=fornecedor_id,
    )
    db.add(produto)
    db.commit()
    return RedirectResponse(url="/admin/produtos", status_code=302)


# ── Editar ────────────────────────────────────────────────────────────────────
@router.get("/produtos/{id}/editar", response_class=HTMLResponse)
def form_editar_produto(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    categorias = db.query(Categoria).order_by(Categoria.nome).all()
    fornecedores = db.query(Fornecedor).order_by(Fornecedor.nome).all()

    imagens_existentes = []
    if os.path.isdir(UPLOAD_DIR):
        imagens_existentes = [
            f"/static/assets/produtos/{f}"
            for f in os.listdir(UPLOAD_DIR)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif"))
        ]

    return templates.TemplateResponse(
        "admin/produtos_form.html",
        {
            "request": request,
            "usuario": usuario,
            "editando": produto,
            "categorias": categorias,
            "fornecedores": fornecedores,
            "imagens_existentes": imagens_existentes,
        },
    )


@router.post("/produtos/{id}/editar")
def editar_produto(
    id: int,
    nome: str = Form(...),
    descricao: str = Form(""),
    preco: float = Form(...),
    tamanho: str = Form(""),
    estoque: int = Form(0),
    categoria_id: int = Form(None),
    fornecedor_id: int = Form(None),
    imagem_existente: str = Form(""),
    imagem: UploadFile = File(None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    novo_caminho = salvar_imagem(imagem)

    produto.nome = nome
    produto.descricao = descricao
    produto.preco = preco
    produto.tamanho = tamanho
    produto.estoque = estoque
    produto.disponivel = estoque > 0
    produto.categoria_id = categoria_id
    produto.fornecedor_id = fornecedor_id
    produto.imagem = novo_caminho or imagem_existente or produto.imagem

    db.commit()
    return RedirectResponse(url="/admin/produtos", status_code=302)


# ── Deletar ───────────────────────────────────────────────────────────────────
@router.post("/produtos/{id}/deletar")
def deletar_produto(
    id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if produto:
        db.delete(produto)
        db.commit()
    return RedirectResponse(url="/admin/produtos", status_code=302)