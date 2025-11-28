from pydantic import BaseModel
from datetime import time


class HorarioBase(BaseModel):
    disciplina_id: int
    hora_comeco: time
    hora_fim: time
    dia_semana: int


class HorarioCreate(HorarioBase):
    pass


class Horario(HorarioBase):
    id: int

    class Config:
        from_attributes = True
