from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import horario as horario_schema
from app.models import horario as horario_model
from app.services.database import get_db

router = APIRouter()


@router.post("", response_model=horario_schema.Horario)
def criar_horario(horario: horario_schema.HorarioCreate, db: Session = Depends(get_db)):
    db_horario = horario_model.Horario(**horario.dict())
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario


@router.get("", response_model=List[horario_schema.Horario])
def listar_horarios(
    usuario_id: Optional[int] = Query(None),
    disciplina_id: Optional[int] = Query(None),
    dia_semana: Optional[int] = Query(None, ge=0, le=6),
    db: Session = Depends(get_db)
):
    query = db.query(horario_model.Horario)
    
    if usuario_id is not None:
        query = query.filter(horario_model.Horario.usuario_id == usuario_id)
    
    if disciplina_id is not None:
        query = query.filter(horario_model.Horario.disciplina_id == disciplina_id)
    
    if dia_semana is not None:
        query = query.filter(horario_model.Horario.dia_semana == dia_semana)
    
    return query.all()


@router.get("/{horario_id}", response_model=horario_schema.Horario)
def obter_horario(horario_id: int, db: Session = Depends(get_db)):
    horario = db.query(horario_model.Horario).filter(horario_model.Horario.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    return horario


@router.put("/{horario_id}", response_model=horario_schema.Horario)
def atualizar_horario(horario_id: int, horario: horario_schema.HorarioCreate, db: Session = Depends(get_db)):
    db_horario = db.query(horario_model.Horario).filter(horario_model.Horario.id == horario_id).first()
    if not db_horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    for key, value in horario.dict().items():
        setattr(db_horario, key, value)
    db.commit()
    db.refresh(db_horario)
    return db_horario


@router.delete("/{horario_id}")
def deletar_horario(horario_id: int, db: Session = Depends(get_db)):
    db_horario = db.query(horario_model.Horario).filter(horario_model.Horario.id == horario_id).first()
    if not db_horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    db.delete(db_horario)
    db.commit()
    return {"message": "Horário deletado"}
