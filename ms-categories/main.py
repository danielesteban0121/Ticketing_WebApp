from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional
from auth.auth import verify_token
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException, RequestValidationError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_422_UNPROCESSABLE_ENTITY

app = FastAPI(
    title="Categories Microservice",
    description="Microservicio encargado de gestionar las categorías de eventos.",
    version="1.0.0"
)

security = HTTPBearer()


# -----------------------------
# MODELOS
# -----------------------------
class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


# Base de datos simulada
categories_db = [
    Category(id=1, name="Concerts", description="Eventos de música y conciertos"),
    Category(id=2, name="Sports", description="Eventos de deportes ")
]


# -----------------------------
# ENDPOINTS
# -----------------------------

@app.post(
    "/categories",
    response_model=Category,
    status_code=status.HTTP_201_CREATED,
    summary="Crea una nueva categoría (requiere Admin)"
)
def create_category(
    category: CategoryCreate,
    token: str = Depends(security),

):
    new_id = len(categories_db) + 1
    new_category = Category(id=new_id, **category.dict())
    categories_db.append(new_category)
    return new_category


@app.get(
    "/categories",
    response_model=List[Category],
    summary="Obtiene todas las categorías"
)
def get_categories():
    return categories_db


@app.get(
    "/categories/{category_id}",
    response_model=Category,
    summary="Obtiene una categoría específica"
)
def get_category(category_id: int):
    for c in categories_db:
        if c.id == category_id:
            return c
    raise HTTPException(status_code=404, detail="Categoría no encontrada")


@app.put(
    "/categories/{category_id}",
    response_model=Category,
    summary="Actualiza una categoría existente (requiere Admin)"
)
def update_category(
    category_id: int,
    data: CategoryCreate,
    token: str = Depends(security),

):
    for index, c in enumerate(categories_db):
        if c.id == category_id:
            updated = Category(id=category_id, **data.dict())
            categories_db[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Categoría no encontrada")


@app.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina una categoría existente (requiere Admin)"
)
def delete_category(
    category_id: int,
    token: str = Depends(security)
):
    for c in categories_db:
        if c.id == category_id:
            categories_db.remove(c)
            return
    raise HTTPException(status_code=404, detail="Categoría no encontrada")


@app.exception_handler(FastAPIHTTPException)
async def custom_http_exception_handler(request, exc):
    # Si el error es 403, devolvemos mensaje personalizado en español
    if exc.status_code == HTTP_403_FORBIDDEN:
        return JSONResponse(
            status_code=HTTP_403_FORBIDDEN,
            content={"detail": "No tienes permisos para realizar esta acción."}
        )

    # Para otros errores, usar el mensaje normal
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Los datos enviados no son válidos. Verifica la información proporcionada."}
    )