from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Busqueda de usuario en la abse de datos por su correo
    user = db.query(User).filter(User.email == form_data.username).first()

    # Si usario no existir o no estar autorizado por Entra ID, aplicar rechazo
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no registrado en el sistema corporativo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Empaquetador de datos en payload del token
    token_data = {
        "sub": user.email,
        "role": user.role
    }

    # Generador de JWT usando security.py
    access_token = create_access_token(data=token_data)

    # Devolucion de token a Frontedn
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }