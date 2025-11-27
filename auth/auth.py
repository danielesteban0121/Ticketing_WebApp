import os
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "DANIELYKEVIN123")

def verify_token(credentials: HTTPAuthorizationCredentials):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado"
        )

    token = credentials.credentials  # FastAPI ya separa "Bearer"

    if token != AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    return True
