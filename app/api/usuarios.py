from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import usuario as usuario_schema
from app.models import usuario as usuario_model
from app.services.database import get_db

router = APIRouter()


@router.post("", response_model=usuario_schema.Usuario)
def criar_usuario(usuario: usuario_schema.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = usuario_model.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.get("", response_model=List[usuario_schema.Usuario])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(usuario_model.Usuario).all()


@router.get("/{usuario_id}", response_model=usuario_schema.Usuario)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuario_model.Usuario).filter(usuario_model.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=usuario_schema.Usuario)
def atualizar_usuario(usuario_id: int, usuario: usuario_schema.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(usuario_model.Usuario).filter(usuario_model.Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    for key, value in usuario.dict().items():
        setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(usuario_model.Usuario).filter(usuario_model.Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(db_usuario)
    db.commit()
    return {"message": "Usuário deletado"}
