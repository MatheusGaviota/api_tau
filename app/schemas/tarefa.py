from pydantic import BaseModel
from datetime import datetime


class TarefaBase(BaseModel):
    titulo: str
    descricao: str
    status: bool
    disciplina_id: int
    data_validade: datetime


class TarefaCreate(TarefaBase):
    pass


class Tarefa(TarefaBase):
    id: int

    class Config:
        from_attributes = True
