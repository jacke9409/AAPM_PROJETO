from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Categoria, Fornecedor, Usuario
from app.routers.auth_router import get_usuario_logado, exigir_admin

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")


# ════════════════════════════════════════════════════════════════
#  CATEGORIAS
# ════════════════════════════════════════════════════════════════

@router.get("/categorias", response_class=HTMLResponse)
def listar_categorias(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_logado),
):
    categorias = db.query(Categoria).order_by(Categoria.nome).all()
    return templates.TemplateResponse(
        "admin/categorias_lista.html",
        {"request": request, "usuario": usuario, "categorias": categorias},
    )


@router.post("/categorias/nova")
def criar_categoria(
    nome: str = Form(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    if not db.query(Categoria).filter(Categoria.nome == nome).first():
        db.add(Categoria(nome=nome))
        db.commit()
    return RedirectResponse(url="/admin/categorias", status_code=302)


@router.post("/categorias/{id}/editar")
def editar_categoria(
    id: int,
    nome: str = Form(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    cat = db.query(Categoria).filter(Categoria.id == id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    cat.nome = nome
    db.commit()
    return RedirectResponse(url="/admin/categorias", status_code=302)


@router.post("/categorias/{id}/deletar")
def deletar_categoria(
    id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    cat = db.query(Categoria).filter(Categoria.id == id).first()
    if cat:
        db.delete(cat)
        db.commit()
    return RedirectResponse(url="/admin/categorias", status_code=302)


# ════════════════════════════════════════════════════════════════
#  FORNECEDORES
# ════════════════════════════════════════════════════════════════

@router.get("/fornecedores", response_class=HTMLResponse)
def listar_fornecedores(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_logado),
):
    fornecedores = db.query(Fornecedor).order_by(Fornecedor.nome).all()
    return templates.TemplateResponse(
        "admin/fornecedores_lista.html",
        {"request": request, "usuario": usuario, "fornecedores": fornecedores},
    )


@router.get("/fornecedores/novo", response_class=HTMLResponse)
def form_novo_fornecedor(
    request: Request,
    usuario: Usuario = Depends(exigir_admin),
):
    return templates.TemplateResponse(
        "admin/fornecedores_form.html",
        {"request": request, "usuario": usuario, "editando": None},
    )


@router.post("/fornecedores/novo")
def criar_fornecedor(
    nome: str = Form(...),
    contato: str = Form(""),
    telefone: str = Form(""),
    email: str = Form(""),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    db.add(Fornecedor(nome=nome, contato=contato, telefone=telefone, email=email))
    db.commit()
    return RedirectResponse(url="/admin/fornecedores", status_code=302)


@router.get("/fornecedores/{id}/editar", response_class=HTMLResponse)
def form_editar_fornecedor(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    editando = db.query(Fornecedor).filter(Fornecedor.id == id).first()
    if not editando:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return templates.TemplateResponse(
        "admin/fornecedores_form.html",
        {"request": request, "usuario": usuario, "editando": editando},
    )


@router.post("/fornecedores/{id}/editar")
def editar_fornecedor(
    id: int,
    nome: str = Form(...),
    contato: str = Form(""),
    telefone: str = Form(""),
    email: str = Form(""),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    f = db.query(Fornecedor).filter(Fornecedor.id == id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    f.nome = nome
    f.contato = contato
    f.telefone = telefone
    f.email = email
    db.commit()
    return RedirectResponse(url="/admin/fornecedores", status_code=302)


@router.post("/fornecedores/{id}/deletar")
def deletar_fornecedor(
    id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    f = db.query(Fornecedor).filter(Fornecedor.id == id).first()
    if f:
        db.delete(f)
        db.commit()
    return RedirectResponse(url="/admin/fornecedores", status_code=302)