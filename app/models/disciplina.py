from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nome = Column(String, nullable=False)
    professor = Column(String, nullable=False)
    sala = Column(String, nullable=False)
    cores = Column(String, nullable=False)
