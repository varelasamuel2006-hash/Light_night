"""
Servicio de geocodificación para Light_night utilizando Geopy y Nominatim.
Permite buscar coordenadas a partir de una ciudad y obtener el nombre legible
mediante geocodificación inversa cuando el usuario utiliza GPS en el navegador.
"""

from typing import Optional, Dict, Any
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

_geolocator = Nominatim(user_agent="light_night_web_app")
_cache_forward: Dict[str, Dict[str, Any]] = {}
_cache_reverse: Dict[str, str] = {}


def geocode_location(query: str) -> Optional[Dict[str, Any]]:
    """
    Busca coordenadas geográficas a partir de un texto (ciudad, pueblo, etc.).
    """
    cleaned = query.strip()
    if not cleaned:
        return None

    key = cleaned.lower()
    if key in _cache_forward:
        return _cache_forward[key]

    try:
        location = _geolocator.geocode(cleaned, timeout=5)
        if location:
            result = {
                "query": cleaned,
                "display_name": location.address,
                "latitude": round(location.latitude, 5),
                "longitude": round(location.longitude, 5)
            }
            _cache_forward[key] = result
            return result
        return None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Error en geocodificación para '{cleaned}': {e}")
        return None


def reverse_geocode(lat: float, lon: float) -> Optional[str]:
    """
    Obtiene el nombre de la ciudad o localidad a partir de coordenadas GPS.
    """
    coord_key = f"{round(lat, 3)},{round(lon, 3)}"
    if coord_key in _cache_reverse:
        return _cache_reverse[coord_key]

    try:
        location = _geolocator.reverse((lat, lon), timeout=5, language="es")
        if location and location.address:
            # Extraer localidad corta o resumen
            addr = location.raw.get("address", {})
            city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality")
            country = addr.get("country")
            short_name = f"{city}, {country}" if city and country else location.address.split(",")[0]
            _cache_reverse[coord_key] = short_name
            return short_name
        return None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Error en reverse geocode: {e}")
        return None
