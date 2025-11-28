from pydantic import BaseModel
from datetime import datetime


class AnotacaoBase(BaseModel):
    titulo: str
    conteudo: str


class AnotacaoCreate(AnotacaoBase):
    pass


class Anotacao(AnotacaoBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True
