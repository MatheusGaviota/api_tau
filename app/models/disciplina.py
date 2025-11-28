from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    professor = Column(String, nullable=False)
    sala = Column(String, nullable=False)
