from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional
from auth.auth import verify_token
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException, RequestValidationError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_422_UNPROCESSABLE_ENTITY

app = FastAPI(
    title="Cities Microservice",
    description="Microservicio encargado de gestionar las ciudades disponibles.",
    version="1.0.0"
)

security = HTTPBearer()


# -----------------------------
# MODELOS
# -----------------------------
class City(BaseModel):
    id: int
    name: str
    country: str
    population: Optional[int] = None


class CityCreate(BaseModel):
    name: str
    country: str
    population: Optional[int] = None


# Base de datos simulada
cities_db = [
    City(id=1, name="Bogotá", country="Colombia", population=7800000),
    City(id=2, name="Medellín", country="Colombia", population=2500000)
]


# -----------------------------
# ENDPOINTS
# -----------------------------

@app.post(
    "/cities",
    response_model=City,
    status_code=status.HTTP_201_CREATED,
    summary="Crea una nueva ciudad (requiere Admin)"
)
def create_city(
    city: CityCreate,
    token: str = Depends(security),
):
    new_id = len(cities_db) + 1
    new_city = City(id=new_id, **city.dict())
    cities_db.append(new_city)
    return new_city


@app.get(
    "/cities",
    response_model=List[City],
    summary="Obtiene todas las ciudades"
)
def get_cities():
    return cities_db


@app.get(
    "/cities/{city_id}",
    response_model=City,
    summary="Obtiene una ciudad específica"
)
def get_city(city_id: int):
    for c in cities_db:
        if c.id == city_id:
            return c
    raise HTTPException(status_code=404, detail="Ciudad no encontrada")


@app.put(
    "/cities/{city_id}",
    response_model=City,
    summary="Actualiza una ciudad existente (requiere Admin)"
)
def update_city(
    city_id: int,
    data: CityCreate,
    token: str = Depends(security)
):
    for index, c in enumerate(cities_db):
        if c.id == city_id:
            updated = City(id=city_id, **data.dict())
            cities_db[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Ciudad no encontrada")


@app.delete(
    "/cities/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina una ciudad existente (requiere Admin)"
)
def delete_city(
    city_id: int,
    token: str = Depends(security)
):
    for c in cities_db:
        if c.id == city_id:
            cities_db.remove(c)
            return
    raise HTTPException(status_code=404, detail="Ciudad no encontrada")


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

