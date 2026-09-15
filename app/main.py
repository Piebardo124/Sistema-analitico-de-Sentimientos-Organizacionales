from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import feedback, auth
from app.api.v1.endpoints import feedback
from app.db.database import engine
from app.db import models
from app.api.v1.endpoints import alerts

#Generador de tablas en base de datos segun models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PluriOne Sentiment Analysis API",
    description="API RESTful para el analisis de sentimientos de comentarios de empleados",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"status": "success", "message": "El middleware esta en funcion"}

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticacion"])
app.include_router(feedback.router, prefix="/api/v1/nlp", tags=["NLP Core"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Gestión de Alertas"])