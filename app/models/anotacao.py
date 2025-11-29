from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.models.base import Base


class Anotacao(Base):
    __tablename__ = "anotacoes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    titulo = Column(String, nullable=False)
    conteudo = Column(String, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
