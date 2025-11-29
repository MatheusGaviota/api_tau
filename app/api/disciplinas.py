from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import disciplina as disciplina_schema
from app.models import disciplina as disciplina_model
from app.services.database import get_db

router = APIRouter()


@router.post("", response_model=disciplina_schema.Disciplina)
def criar_disciplina(disciplina: disciplina_schema.DisciplinaCreate, db: Session = Depends(get_db)):
    db_disciplina = disciplina_model.Disciplina(**disciplina.dict())
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina


@router.get("", response_model=List[disciplina_schema.Disciplina])
def listar_disciplinas(usuario_id: int = None, db: Session = Depends(get_db)):
    query = db.query(disciplina_model.Disciplina)
    if usuario_id is not None:
        query = query.filter(disciplina_model.Disciplina.usuario_id == usuario_id)
    return query.all()


@router.get("/{disciplina_id}", response_model=disciplina_schema.Disciplina)
def obter_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    disciplina = db.query(disciplina_model.Disciplina).filter(disciplina_model.Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina


@router.put("/{disciplina_id}", response_model=disciplina_schema.Disciplina)
def atualizar_disciplina(disciplina_id: int, disciplina: disciplina_schema.DisciplinaCreate, db: Session = Depends(get_db)):
    db_disciplina = db.query(disciplina_model.Disciplina).filter(disciplina_model.Disciplina.id == disciplina_id).first()
    if not db_disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    for key, value in disciplina.dict().items():
        setattr(db_disciplina, key, value)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina


@router.delete("/{disciplina_id}")
def deletar_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    db_disciplina = db.query(disciplina_model.Disciplina).filter(disciplina_model.Disciplina.id == disciplina_id).first()
    if not db_disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    db.delete(db_disciplina)
    db.commit()
    return {"message": "Disciplina deletada"}
