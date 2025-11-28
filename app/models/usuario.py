from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    senha = Column(String, nullable=False)
