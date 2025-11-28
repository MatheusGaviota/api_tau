from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.models.base import Base


class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)
    data_validade = Column(DateTime, nullable=False)
