from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.schemas import tarefa as tarefa_schema
from app.models import tarefa as tarefa_model
from app.services.database import get_db

router = APIRouter()


@router.post("", response_model=tarefa_schema.Tarefa)
def criar_tarefa(tarefa: tarefa_schema.TarefaCreate, db: Session = Depends(get_db)):
    db_tarefa = tarefa_model.Tarefa(**tarefa.dict())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa


@router.get("", response_model=List[tarefa_schema.Tarefa])
def listar_tarefas(
    usuario_id: Optional[int] = Query(None),
    disciplina_id: Optional[int] = Query(None),
    status: Optional[bool] = Query(None),
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(tarefa_model.Tarefa)
    
    if usuario_id is not None:
        query = query.filter(tarefa_model.Tarefa.usuario_id == usuario_id)
    
    if disciplina_id is not None:
        query = query.filter(tarefa_model.Tarefa.disciplina_id == disciplina_id)
    
    if status is not None:
        query = query.filter(tarefa_model.Tarefa.status == status)
    
    if data_inicio is not None:
        query = query.filter(tarefa_model.Tarefa.data_validade >= data_inicio)
    
    if data_fim is not None:
        query = query.filter(tarefa_model.Tarefa.data_validade <= data_fim)
    
    return query.all()


@router.get("/{tarefa_id}", response_model=tarefa_schema.Tarefa)
def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(tarefa_model.Tarefa).filter(tarefa_model.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


@router.put("/{tarefa_id}", response_model=tarefa_schema.Tarefa)
def atualizar_tarefa(tarefa_id: int, tarefa: tarefa_schema.TarefaCreate, db: Session = Depends(get_db)):
    db_tarefa = db.query(tarefa_model.Tarefa).filter(tarefa_model.Tarefa.id == tarefa_id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    for key, value in tarefa.dict().items():
        setattr(db_tarefa, key, value)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa


@router.delete("/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    db_tarefa = db.query(tarefa_model.Tarefa).filter(tarefa_model.Tarefa.id == tarefa_id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(db_tarefa)
    db.commit()
    return {"message": "Tarefa deletada"}
