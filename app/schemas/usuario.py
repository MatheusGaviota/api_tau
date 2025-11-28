from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    senha: str


class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
