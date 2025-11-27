from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from auth.auth import verify_token
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException, RequestValidationError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_422_UNPROCESSABLE_ENTITY

# Security scheme for Swagger
auth_scheme = HTTPBearer()

app = FastAPI(
    title="Puntos de venta Ticketing WebApp",
    swagger_ui_parameters={"persistAuthorization": True},
    openapi_tags=[
        {"name": "Puntos de venta"}
    ]
)

# ---------------------------------------------------
# Model
# ---------------------------------------------------
class PointOfSale(BaseModel):
    id: int
    name: str
    city_id: int
    address: str

# Fake database
points_db = [
    {"id": 1, "name": "Main Store", "city_id": 1, "address": "Street 123"},
    {"id": 2, "name": "Branch Store", "city_id": 2, "address": "Avenue 45"},
]

# ---------------------------------------------------
# Endpoints
# ---------------------------------------------------

# Create (Admin)
@app.post(
    "/points-of-sale",
    status_code=status.HTTP_201_CREATED,
    tags=["Puntos de venta"],
    summary="Crear un punto de venta",
    description="Crea un nuevo punto de venta (requiere administrador)."
)
def create_point_of_sale(
    point: PointOfSale,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    verify_token(token.credentials)

    for p in points_db:
        if p["id"] == point.id:
            raise HTTPException(status_code=400, detail="Este punto de venta ya existe")

    points_db.append(point.dict())
    return {"message": "Punto de venta creado satisfactoriamente", "data": point}


# Get all (No Auth)
@app.get(
    "/points-of-sale",
    status_code=status.HTTP_200_OK,
    tags=["Puntos de venta"],
    summary="Obtener todos los puntos de venta",
    description="Devuelve la lista completa de puntos de venta registrados."
)
def get_all_points():
    return {"results": points_db}


# Get one (No Auth)
@app.get(
    "/points-of-sale/{point_id}",
    status_code=status.HTTP_200_OK,
    tags=["Puntos de venta"],
    summary="Obtener un punto de venta por ID",
    description="Devuelve la información de un punto de venta específico."
)
def get_point(point_id: int):
    for p in points_db:
        if p["id"] == point_id:
            return p
    raise HTTPException(status_code=404, detail="Punto de venta no encontrado")


# Update (Admin)
@app.put(
    "/points-of-sale/{point_id}",
    status_code=status.HTTP_200_OK,
    tags=["Puntos de venta"],
    summary="Actualizar un punto de venta",
    description="Actualiza la información de un punto de venta existente (requiere administrador)."
)
def update_point(
    point_id: int,
    data: PointOfSale,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    verify_token(token.credentials)

    for index, p in enumerate(points_db):
        if p["id"] == point_id:
            points_db[index] = data.dict()
            return {"message": "Punto de venta actualizado satisfactoriamente", "data": data}

    raise HTTPException(status_code=404, detail="Punto de venta no encontrado")


# Delete (Admin)
@app.delete(
    "/points-of-sale/{point_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Puntos de venta"],
    summary="Eliminar un punto de venta",
    description="Elimina un punto de venta por ID (requiere administrador)."
)
def delete_point(
    point_id: int,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    verify_token(token.credentials)

    for p in points_db:
        if p["id"] == point_id:
            points_db.remove(p)
            return

    raise HTTPException(status_code=404, detail="Punto de venta no encontrado")


# ---------------------------------------------------
# Custom error messages
# ---------------------------------------------------
@app.exception_handler(FastAPIHTTPException)
async def custom_http_exception_handler(request, exc):
    # Error 403 en español
    if exc.status_code == HTTP_403_FORBIDDEN:
        return JSONResponse(
            status_code=HTTP_403_FORBIDDEN,
            content={"detail": "No tienes permisos para realizar esta acción."}
        )

    # Resto de errores tal cual
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