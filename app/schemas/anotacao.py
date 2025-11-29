from pydantic import BaseModel
from datetime import datetime


class AnotacaoBase(BaseModel):
    usuario_id: int
    titulo: str
    conteudo: str


class AnotacaoCreate(AnotacaoBase):
    pass


class Anotacao(AnotacaoBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True
