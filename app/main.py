from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.routes import router
from app.services.database import engine
from app.models.base import Base
from app.models import usuario, anotacao, disciplina, tarefa, horario

app = FastAPI(title="API Tau", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Tau</title>
    </head>
    <body>
        <h1>API Tau</h1>
        <p><a href="/docs">Swagger Documentation</a></p>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
