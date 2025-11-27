import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException, Header, status
from pydantic import BaseModel
from typing import Optional
from auth.auth import verify_token

app = FastAPI(
    title="Points of Sale Microservice",
    description="Microservicio encargado de gestionar los puntos de venta.",
    version="1.0.0"
)

print("🚀 [RENDER] Points of Sale Microservice iniciando...")

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

# Endpoints

@app.post(
    "/points-of-sale",
    status_code=status.HTTP_201_CREATED,
    summary="Crear un punto de venta",
    description="Crea un nuevo punto de venta (requiere administrador)."
)
def create_point_of_sale(
    point: PointOfSale,
    authorization: str = Header(None)
):
    verify_token(authorization)

    for p in points_db:
        if p["id"] == point.id:
            raise HTTPException(status_code=400, detail="Este punto de venta ya existe")

    points_db.append(point.dict())
    return {"message": "Punto de venta creado satisfactoriamente", "data": point}


@app.get(
    "/points-of-sale",
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los puntos de venta",
    description="Devuelve la lista completa de puntos de venta registrados."
)
def get_all_points():
    return {"results": points_db}


@app.get(
    "/points-of-sale/{point_id}",
    status_code=status.HTTP_200_OK,
    summary="Obtener un punto de venta por ID",
    description="Devuelve la información de un punto de venta específico."
)
def get_point(point_id: int):
    for p in points_db:
        if p["id"] == point_id:
            return p
    raise HTTPException(status_code=404, detail="Punto de venta no encontrado")


@app.put(
    "/points-of-sale/{point_id}",
    status_code=status.HTTP_200_OK,
    summary="Actualizar un punto de venta",
    description="Actualiza la información de un punto de venta existente (requiere administrador)."
)
def update_point(
    point_id: int,
    data: PointOfSale,
    authorization: str = Header(None)
):
    verify_token(authorization)

    for index, p in enumerate(points_db):
        if p["id"] == point_id:
            points_db[index] = data.dict()
            return {"message": "Punto de venta actualizado satisfactoriamente", "data": data}

    raise HTTPException(status_code=404, detail="Punto de venta no encontrado")


@app.delete(
    "/points-of-sale/{point_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un punto de venta",
    description="Elimina un punto de venta por ID (requiere administrador)."
)
def delete_point(
    point_id: int,
    authorization: str = Header(None)
):
    verify_token(authorization)

    for p in points_db:
        if p["id"] == point_id:
            points_db.remove(p)
            return

    raise HTTPException(status_code=404, detail="Punto de venta no encontrado")


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check"
)
def health_check():
    """Endpoint de salud para monitoreo en Render."""
    return {"status": "ok", "service": "points-of-sale"}


@app.on_event("startup")
async def startup_event():
    """Evento de inicio del servicio."""
    print("✅ [RENDER] Points of Sale Microservice está listo.")