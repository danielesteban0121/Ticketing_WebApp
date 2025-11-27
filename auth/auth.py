from fastapi import HTTPException, Header, status
from pydantic import BaseModel

# ============================
#  ADMIN POR DEFECTO
# ============================
DEFAULT_ADMIN = "KevinYDaniel123"

# ============================
#  TOKEN GLOBAL
# ============================
AUTH_TOKEN = "DANIELYKEVIN123"

# Estructura opcional para futuros usuarios
class User(BaseModel):
    username: str
    password: str

# ============================
#  VALIDADOR DE TOKEN
# ============================
def verify_token(auth_token: str = Header(None)):
    if auth_token != AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o no proporcionado"
        )
    return True
