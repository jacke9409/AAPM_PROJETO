from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    comprador_nome = Column(String(150), nullable=False)
    total = Column(Float, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    usuario = relationship("Usuario", back_populates="vendas")
    itens = relationship("ItemVenda", back_populates="venda")


class ItemVenda(Base):
    __tablename__ = "itens_venda"

    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    venda_id = Column(Integer, ForeignKey("vendas.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)

    venda = relationship("Venda", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_venda")


class Nota(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    conteudo = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="notas")