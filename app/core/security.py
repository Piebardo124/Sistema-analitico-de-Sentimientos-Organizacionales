import os
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Llave para firmar los tokens
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "plurione_super_secret_key_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8 # Cumlimiento de arquitectura.

# Esquema de autenticacion para FastAPI
oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def create_acces_token(data: dict):
    """Genera un token JWT con una expiracion de 8 horas"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def varify_token(token: str = Depends(oauth2_schema)):
    """Valida el token en cada peticion y extrae el rol del usuario"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_AUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")

        if email is None or role is None:
            raise credentials_exception

        return {"email": email, "role": role}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesion de 8 horas expiro, Inicia sesion nuevamente."
        )
    except jwt.InvalidTokenError:
        raise credentials_exception
    