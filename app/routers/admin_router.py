from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario, RoleEnum, Venda, Nota
from app.routers.auth_router import get_usuario_logado, exigir_admin, gerar_hash

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")


# ── Dashboard ─────────────────────────────────────────────────────────────────
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_logado),
):
    total_vendas = db.query(Venda).count()
    receita_total = db.query(Venda).all()
    receita = sum(v.total for v in receita_total)

    ultimas_vendas = (
        db.query(Venda).order_by(Venda.criado_em.desc()).limit(5).all()
    )
    notas = (
        db.query(Nota)
        .filter(Nota.usuario_id == usuario.id)
        .order_by(Nota.criado_em.desc())
        .limit(5)
        .all()
    )

    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "usuario": usuario,
            "total_vendas": total_vendas,
            "receita": receita,
            "ultimas_vendas": ultimas_vendas,
            "notas": notas,
        },
    )


# ── Usuários (só ADMIN) ───────────────────────────────────────────────────────
@router.get("/usuarios", response_class=HTMLResponse)
def listar_usuarios(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    usuarios = db.query(Usuario).order_by(Usuario.nome).all()
    return templates.TemplateResponse(
        "admin/usuarios_lista.html",
        {"request": request, "usuario": usuario, "usuarios": usuarios},
    )


@router.get("/usuarios/novo", response_class=HTMLResponse)
def form_novo_usuario(
    request: Request,
    usuario: Usuario = Depends(exigir_admin),
):
    return templates.TemplateResponse(
        "admin/usuarios_form.html",
        {"request": request, "usuario": usuario, "editando": None},
    )


@router.post("/usuarios/novo")
def criar_usuario(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    if db.query(Usuario).filter(Usuario.email == email).first():
        return templates.TemplateResponse(
            "admin/usuarios_form.html",
            {
                "request": request,
                "usuario": usuario,
                "editando": None,
                "erro": "E-mail já cadastrado",
            },
            status_code=400,
        )

    novo = Usuario(
        nome=nome,
        email=email,
        senha_hash=gerar_hash(senha),
        role=RoleEnum(role),
    )
    db.add(novo)
    db.commit()
    return RedirectResponse(url="/admin/usuarios", status_code=302)


@router.get("/usuarios/{id}/editar", response_class=HTMLResponse)
def form_editar_usuario(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    editando = db.query(Usuario).filter(Usuario.id == id).first()
    if not editando:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return templates.TemplateResponse(
        "admin/usuarios_form.html",
        {"request": request, "usuario": usuario, "editando": editando},
    )


@router.post("/usuarios/{id}/editar")
def editar_usuario(
    id: int,
    nome: str = Form(...),
    email: str = Form(...),
    role: str = Form(...),
    senha: str = Form(""),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    editando = db.query(Usuario).filter(Usuario.id == id).first()
    if not editando:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    editando.nome = nome
    editando.email = email
    editando.role = RoleEnum(role)
    if senha:
        editando.senha_hash = gerar_hash(senha)

    db.commit()
    return RedirectResponse(url="/admin/usuarios", status_code=302)


@router.post("/usuarios/{id}/deletar")
def deletar_usuario(
    id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_admin),
):
    u = db.query(Usuario).filter(Usuario.id == id).first()
    if u:
        db.delete(u)
        db.commit()
    return RedirectResponse(url="/admin/usuarios", status_code=302)


# ── Notas ─────────────────────────────────────────────────────────────────────
@router.get("/notas", response_class=HTMLResponse)
def listar_notas(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_logado),
):
    notas = (
        db.query(Nota)
        .filter(Nota.usuario_id == usuario.id)
        .order_by(Nota.criado_em.desc())
        .all()
    )
    return templates.TemplateResponse(
        "admin/notas.html",
        {"request": request, "usuario": usuario, "notas": notas},
    )


@router.post("/notas/nova")
def criar_nota(
    titulo: str = Form(...),
    conteudo: str = Form(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_logado),
):
    nota = Nota(titulo=titulo, conteudo=conteudo, usuario_id=usuario.id)
    db.add(nota)
    db.commit()
    return RedirectResponse(url="/admin/notas", status_code=302)


@router.post("/notas/{id}/deletar")
def deletar_nota(
    id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_logado),
):
    nota = db.query(Nota).filter(Nota.id == id, Nota.usuario_id == usuario.id).first()
    if nota:
        db.delete(nota)
        db.commit()
    return RedirectResponse(url="/admin/notas", status_code=302)