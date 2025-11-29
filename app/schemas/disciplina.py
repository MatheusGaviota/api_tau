from pydantic import BaseModel


class DisciplinaBase(BaseModel):
    nome: str
    professor: str
    sala: str
    cores: str


class DisciplinaCreate(DisciplinaBase):
    pass


class Disciplina(DisciplinaBase):
    id: int

    class Config:
        from_attributes = True
