from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(String(500), nullable=True)
    preco = Column(Float, nullable=False)
    tamanho = Column(String(50), nullable=True)
    estoque = Column(Integer, default=0)
    disponivel = Column(Boolean, default=True)
    imagem = Column(String(255), nullable=True)

    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    categoria = relationship("Categoria", back_populates="produtos")
    fornecedor = relationship("Fornecedor", back_populates="produtos")
    itens_venda = relationship("ItemVenda", back_populates="produto")