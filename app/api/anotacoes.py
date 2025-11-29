from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.schemas import anotacao as anotacao_schema
from app.models import anotacao as anotacao_model
from app.services.database import get_db

router = APIRouter()


@router.post("", response_model=anotacao_schema.Anotacao)
def criar_anotacao(anotacao: anotacao_schema.AnotacaoCreate, db: Session = Depends(get_db)):
    db_anotacao = anotacao_model.Anotacao(**anotacao.dict())
    db.add(db_anotacao)
    db.commit()
    db.refresh(db_anotacao)
    return db_anotacao


@router.get("", response_model=List[anotacao_schema.Anotacao])
def listar_anotacoes(
    usuario_id: Optional[int] = Query(None),
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(anotacao_model.Anotacao)
    
    if usuario_id is not None:
        query = query.filter(anotacao_model.Anotacao.usuario_id == usuario_id)
    
    if data_inicio is not None:
        query = query.filter(anotacao_model.Anotacao.data_criacao >= data_inicio)
    
    if data_fim is not None:
        query = query.filter(anotacao_model.Anotacao.data_criacao <= data_fim)
    
    return query.all()


@router.get("/{anotacao_id}", response_model=anotacao_schema.Anotacao)
def obter_anotacao(anotacao_id: int, db: Session = Depends(get_db)):
    anotacao = db.query(anotacao_model.Anotacao).filter(anotacao_model.Anotacao.id == anotacao_id).first()
    if not anotacao:
        raise HTTPException(status_code=404, detail="Anotação não encontrada")
    return anotacao


@router.put("/{anotacao_id}", response_model=anotacao_schema.Anotacao)
def atualizar_anotacao(anotacao_id: int, anotacao: anotacao_schema.AnotacaoCreate, db: Session = Depends(get_db)):
    db_anotacao = db.query(anotacao_model.Anotacao).filter(anotacao_model.Anotacao.id == anotacao_id).first()
    if not db_anotacao:
        raise HTTPException(status_code=404, detail="Anotação não encontrada")
    for key, value in anotacao.dict().items():
        setattr(db_anotacao, key, value)
    db.commit()
    db.refresh(db_anotacao)
    return db_anotacao


@router.delete("/{anotacao_id}")
def deletar_anotacao(anotacao_id: int, db: Session = Depends(get_db)):
    db_anotacao = db.query(anotacao_model.Anotacao).filter(anotacao_model.Anotacao.id == anotacao_id).first()
    if not db_anotacao:
        raise HTTPException(status_code=404, detail="Anotação não encontrada")
    db.delete(db_anotacao)
    db.commit()
    return {"message": "Anotação deletada"}
