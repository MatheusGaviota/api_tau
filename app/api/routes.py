from fastapi import APIRouter
from app.api import usuarios, anotacoes, disciplinas, tarefas, horarios

router = APIRouter()

router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
router.include_router(anotacoes.router, prefix="/anotacoes", tags=["anotacoes"])
router.include_router(disciplinas.router, prefix="/disciplinas", tags=["disciplinas"])
router.include_router(tarefas.router, prefix="/tarefas", tags=["tarefas"])
router.include_router(horarios.router, prefix="/horarios", tags=["horarios"])
