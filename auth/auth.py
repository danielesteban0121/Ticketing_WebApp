import os
from fastapi import HTTPException, status

# ============================
#  TOKEN DE AUTENTICACIÓN
# ============================
# En Render, usar variable de entorno AUTH_TOKEN
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "DANIELYKEVIN123")

# ============================
#  VALIDADOR DE TOKEN
# ============================
def verify_token(token: str = None) -> bool:
    """Valida el token de autenticación."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado o inválido"
        )
    
    # Si viene "Bearer TOKEN", extrae solo el token
    if token.startswith("Bearer "):
        token = token[7:]
    
    if token != AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    return True
