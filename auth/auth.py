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
def verify_token(token: str) -> bool:
    """Valida el token de autenticación."""
    if token != AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o no proporcionado"
        )
    return True
