from sqlalchemy import Column, Integer, Time, ForeignKey
from app.models.base import Base


class Horario(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)
    hora_comeco = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    dia_semana = Column(Integer, nullable=False)
