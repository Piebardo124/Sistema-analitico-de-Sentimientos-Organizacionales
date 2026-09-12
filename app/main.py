from fastapi import FastAPI
from app.api.v1.endpoints import feedback
from app.db.database import engine
from app.db import models

#Generador de tablas en base de datos segun models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PluriOne Sentiment Analysis API",
    description="API RESTful para el analisis de sentimientos de comentarios de empleados",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "success", "message": "El middleware esta en funcion"}

app.include_router(feedback.router, prefix="/api/v1/nlp", tags=["NLP Core"])