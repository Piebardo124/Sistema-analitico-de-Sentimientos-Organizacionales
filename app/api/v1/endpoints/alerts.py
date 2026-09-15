import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.db.database import get_db
from app.core.security import verify_token
from app.db.models import Alert

router = APIRouter()

# Esquema de salida 
class AlertResponse(BaseModel):
    id: int
    feedback_id: uuid.UUID
    risk_level: str
    reason: str
    status: str

    class Config:
        from_attributes = True

# EndPoit
@router.get("/", response_model=List[AlertResponse])
def list_alerts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token) # Token valido
):
    """
    Lista todas las laertas generadas por el sistema.
    Acceso restringido a roles de Administracion y RH
    """
    # Validacion que el usuario tenga el rol correcto.
    rol_usuario = current_user.get("role")
    if rol_usuario not in ["admin", "hr"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo Recursos Humanos y Administradores pueden ver la bandeja"
        )

    # Consulta a PostgreSQL
    # Alertas ordenadas
    alerts = db.query(Alert).all()

    # Retorno de lista
    return alerts






















