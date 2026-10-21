"""
Servidor web FastAPI para Light_night.
Expone API REST para cálculos astronómicos, geocodificación y sirve la interfaz web interactiva.
"""

from datetime import datetime
from typing import Optional
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from core.astronomy import get_sky_snapshot
from core.celestial_catalog import get_all_constellations_summary, get_constellation_by_id
from core.geocoding import geocode_location, reverse_geocode

app = FastAPI(
    title="Light Night - Observatorio de Constelaciones",
    description="API astronómica para la visualización de constelaciones y estrellas en tiempo real.",
    version="1.0.0"
)

# Habilitar CORS para desarrollo local flexible
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SkyRequest(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitud del observador (-90 a 90)")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitud del observador (-180 a 180)")
    datetime_iso: Optional[str] = Field(None, description="Fecha y hora en formato ISO 8601 (opcional)")
    min_altitude: float = Field(0.0, ge=-20.0, le=90.0, description="Altitud mínima sobre el horizonte en grados")
    constellation: Optional[str] = Field(None, description="Identificador de constelación a filtrar o resaltar")


class GeocodeRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Nombre de ciudad, pueblo o lugar a buscar")


class ReverseGeocodeRequest(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "Light_night", "version": "1.0.0"}


@app.get("/api/constellations")
def list_constellations():
    """Devuelve el catálogo de constelaciones disponibles."""
    return {
        "status": "success",
        "constellations": get_all_constellations_summary()
    }


@app.post("/api/sky")
def compute_sky(req: SkyRequest):
    """Calcula las posiciones de estrellas y constelaciones visibles para la ubicación y fecha dadas."""
    dt = None
    if req.datetime_iso:
        try:
            # Reemplazar Z si existe para consistencia con fromisoformat
            clean_iso = req.datetime_iso.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean_iso)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=f"Formato de fecha inválido: {err}")

    try:
        snapshot = get_sky_snapshot(
            lat=req.latitude,
            lon=req.longitude,
            dt=dt,
            min_altitude=req.min_altitude,
            filter_constellation=req.constellation
        )
        return snapshot
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error al calcular posiciones astronómicas: {err}")


@app.post("/api/geocode")
def geocode_city(req: GeocodeRequest):
    """Busca una ubicación por nombre y devuelve sus coordenadas geográficas."""
    result = geocode_location(req.query)
    if not result:
        return {
            "success": False,
            "message": f"No se encontró la ubicación '{req.query}'. Comprueba el nombre o escribe una ciudad cercana."
        }
    return {
        "success": True,
        "data": result
    }


@app.post("/api/reverse-geocode")
def reverse_geocode_coords(req: ReverseGeocodeRequest):
    """Convierte coordenadas GPS a un nombre de localidad legible."""
    name = reverse_geocode(req.latitude, req.longitude)
    return {
        "success": bool(name),
        "display_name": name or f"Lat: {round(req.latitude, 3)}, Lon: {round(req.longitude, 3)}"
    }


# Montar carpeta estática para la interfaz web
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
