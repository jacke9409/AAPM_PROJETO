from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    FUNCIONARIO = "FUNCIONARIO"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.FUNCIONARIO, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    vendas = relationship("Venda", back_populates="usuario")
    notas = relationship("Nota", back_populates="usuario")