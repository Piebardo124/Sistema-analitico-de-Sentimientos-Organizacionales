import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext

from app.db.database import get_db
from app.db.models import User
from app.core.security import create_access_token

router = APIRouter()

# Configuracion de motor de encriptacion (Borrar mas adelante)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema para registrar al admin 
class UserRegister(BaseModel):
    email: str
    password:str

# Endpoint de RegistroLocal
@router.post("/register-admin")
def create_admin_user(user: UserRegister, db: Session = Depends(get_db)):
    """Crea un usuario administrador inicial para pruebas locales"""

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya esta registrado")

    # Encriptamiento de contraseña antes de guardado
    hashed_pw = pwd_context.hash(user.password)
    new_admin = User(
        user_id=str (uuid.uuid4()),
        email=user.email,
        role="admin",
        hashed_password=hashed_pw
    )
    db.add(new_admin)
    db.commit()
    return {"message": "¡Administrador creado exitosamente! Ya puedes iniciar sesión."}

# Endpoint de Login (Desarrollo local de mientras)
@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Busqueda de usuario en la abse de datos por su correo
    user = db.query(User).filter(User.email == form_data.username).first()

    # Si usario no existir o no estar autorizado por Entra ID, aplicar rechazo
    if not user or not user.hashed_password or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
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