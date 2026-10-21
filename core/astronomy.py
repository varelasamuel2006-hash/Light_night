"""
Motor astronómico para Light_night utilizando Skyfield y efemérides JPL de421.bsp.
Calcula la posición instantánea (Altitud, Azimut, visibilidad y coordenadas de proyección)
de estrellas y constelaciones para una latitud, longitud y fecha/hora dadas.
"""

import math
import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from skyfield.api import Loader, Topos, Star
from .celestial_catalog import CONSTELLATIONS, BRIGHT_NAVIGATIONAL_STARS, get_constellation_by_id

# Directorio de efemérides (reutiliza ~/skyfield_data del proyecto original)
DATA_DIR = os.path.expanduser('~/skyfield_data')
os.makedirs(DATA_DIR, exist_ok=True)

load = Loader(DATA_DIR)
ts = load.timescale()
eph = load('de421.bsp')
earth = eph['earth']


def _compute_projection(alt_deg: float, az_deg: float):
    """
    Calcula la proyección azimutal cenital del cielo (Planisferio).
    Cénit (alt = 90°) -> radio = 0 (centro del domo).
    Horizonte (alt = 0°) -> radio = 1.0 (perímetro).
    Orientación astronómica mirando arriba:
    Norte = Arriba (0°), Este = Izquierda (90°), Sur = Abajo (180°), Oeste = Derecha (270°).
    """
    r = max(0.0, (90.0 - alt_deg) / 90.0)
    az_rad = math.radians(az_deg)
    proj_x = -r * math.sin(az_rad)
    proj_y = -r * math.cos(az_rad)

    return proj_x, proj_y


def compute_star_position(observador, t, star_info: Dict[str, Any], min_altitude: float = 0.0):
    """Calcula las coordenadas horizontales de una estrella."""
    star = Star(ra_hours=star_info["ra"], dec_degrees=star_info["dec"])
    astrometric = observador.at(t).observe(star)
    apparent = astrometric.apparent()
    alt, az, _ = apparent.altaz()

    alt_deg = float(alt.degrees)
    az_deg = float(az.degrees)
    visible = alt_deg >= min_altitude

    proj_x, proj_y = _compute_projection(alt_deg, az_deg)

    return {
        "nombre": star_info["nombre"],
        "constelacion": star_info.get("constelacion", ""),
        "ra": float(star_info["ra"]),
        "dec": float(star_info["dec"]),
        "mag": float(star_info.get("mag", 3.0)),
        "color": star_info.get("color", "#ffffff"),
        "tipo": star_info.get("tipo", "Estrella"),
        "alt": round(alt_deg, 2),
        "az": round(az_deg, 2),
        "visible": bool(visible),
        "proj_x": round(float(proj_x), 4),
        "proj_y": round(float(proj_y), 4)
    }


def get_sky_snapshot(
    lat: float,
    lon: float,
    dt: Optional[datetime] = None,
    min_altitude: float = 0.0,
    filter_constellation: Optional[str] = None
) -> Dict[str, Any]:
    """
    Obtiene la instantánea completa del cielo nocturno para la ubicación y fecha seleccionada.
    """
    ubicacion = Topos(latitude_degrees=lat, longitude_degrees=lon)
    observador = earth + ubicacion

    # Manejo de tiempo
    if dt is None:
        t = ts.now()
    else:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        t = ts.from_datetime(dt)

    selected_constellations = {}
    if filter_constellation:
        found = get_constellation_by_id(filter_constellation)
        if found:
            selected_constellations[found["id"]] = found
        else:
            selected_constellations = CONSTELLATIONS
    else:
        selected_constellations = CONSTELLATIONS

    processed_constellations = []
    all_visible_stars_count = 0
    stars_lookup = {}

    for c_id, c_data in selected_constellations.items():
        const_stars = []
        visible_const_stars = []

        for s_info in c_data["stars"]:
            s_dict = dict(s_info)
            s_dict["constelacion"] = c_data["name"]
            computed = compute_star_position(observador, t, s_dict, min_altitude)
            const_stars.append(computed)
            stars_lookup[computed["nombre"]] = computed

            if computed["visible"]:
                visible_const_stars.append(computed)
                all_visible_stars_count += 1

        # Conexiones válidas entre estrellas
        valid_lines = []
        for origen, destino in c_data.get("conexiones", []):
            e1 = stars_lookup.get(origen)
            e2 = stars_lookup.get(destino)
            if e1 and e2 and (e1["visible"] or e2["visible"]):
                valid_lines.append({
                    "origen": origen,
                    "destino": destino,
                    "origen_pos": {"x": e1["proj_x"], "y": e1["proj_y"], "alt": e1["alt"], "az": e1["az"]},
                    "destino_pos": {"x": e2["proj_x"], "y": e2["proj_y"], "alt": e2["alt"], "az": e2["az"]},
                    "ambas_visibles": bool(e1["visible"] and e2["visible"])
                })

        processed_constellations.append({
            "id": c_data["id"],
            "name": c_data["name"],
            "latin_name": c_data["latin_name"],
            "season": c_data["season"],
            "description": c_data["description"],
            "total_stars": len(c_data["stars"]),
            "visible_stars_count": len(visible_const_stars),
            "is_visible": len(visible_const_stars) > 0,
            "stars": const_stars,
            "lines": valid_lines
        })

    # Estrellas de referencia y fondo brillante
    bright_stars = []
    for s_info in BRIGHT_NAVIGATIONAL_STARS:
        comp = compute_star_position(observador, t, s_info, min_altitude)
        if comp["visible"]:
            bright_stars.append(comp)

    processed_constellations.sort(key=lambda c: c["visible_stars_count"], reverse=True)

    utc_cal = t.utc
    return {
        "status": "success",
        "observer": {
            "latitude": float(lat),
            "longitude": float(lon)
        },
        "time": {
            "utc_iso": str(t.utc_iso()),
            "year": int(utc_cal.year),
            "month": int(utc_cal.month),
            "day": int(utc_cal.day),
            "hour": int(utc_cal.hour),
            "minute": int(utc_cal.minute)
        },
        "min_altitude": float(min_altitude),
        "total_visible_stars": int(all_visible_stars_count + len(bright_stars)),
        "constellations": processed_constellations,
        "bright_navigational_stars": bright_stars
    }
