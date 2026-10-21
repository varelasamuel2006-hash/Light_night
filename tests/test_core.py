import sys
import os

# Asegurar path correcto
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from core.astronomy import get_sky_snapshot
from core.geocoding import geocode_location, reverse_geocode
from core.celestial_catalog import get_all_constellations_summary
from datetime import datetime, timezone

def test_all():
    print("--- Test 1: Catálogo de constelaciones ---")
    consts = get_all_constellations_summary()
    assert len(consts) == 12, f"Esperadas 12 constelaciones, obtenidas {len(consts)}"
    print(f"✓ Éxito: {len(consts)} constelaciones cargadas correctamente.")

    print("\n--- Test 2: Geocodificación directa (Madrid) ---")
    madrid = geocode_location("Madrid")
    assert madrid and "latitude" in madrid, "Fallo en geocodificación"
    print(f"✓ Éxito: Madrid en {madrid['latitude']}°, {madrid['longitude']}° ({madrid['display_name']})")

    print("\n--- Test 3: Geocodificación inversa ---")
    rev = reverse_geocode(40.4168, -3.7038)
    assert rev, "Fallo en geocodificación inversa"
    print(f"✓ Éxito: Localidad detectada: {rev}")

    print("\n--- Test 4: Cálculo astronómico en tiempo actual ---")
    snap = get_sky_snapshot(40.4168, -3.7038)
    assert snap["status"] == "success"
    assert snap["total_visible_stars"] > 0
    print(f"✓ Éxito: {snap['total_visible_stars']} estrellas visibles calculadas.")
    print(f"  Constelación destacada: {snap['constellations'][0]['name']} con {snap['constellations'][0]['visible_stars_count']} estrellas visibles.")

    print("\n--- Test 5: Cálculo astronómico en fecha futura (Solsticio de invierno) ---")
    dt_winter = datetime(2026, 12, 21, 23, 0, 0, tzinfo=timezone.utc)
    snap_winter = get_sky_snapshot(40.4168, -3.7038, dt=dt_winter)
    assert snap_winter["status"] == "success"
    print(f"✓ Éxito: {snap_winter['total_visible_stars']} estrellas visibles en solsticio de invierno.")

    print("\n--- Test 6: Filtro específico por constelación (Orión) ---")
    snap_orion = get_sky_snapshot(40.4168, -3.7038, dt=dt_winter, filter_constellation="orion")
    assert len(snap_orion["constellations"]) == 1
    orion = snap_orion["constellations"][0]
    assert orion["name"] == "Orión"
    assert len(orion["lines"]) > 0
    print(f"✓ Éxito: Orión filtrado con {orion['total_stars']} estrellas y {len(orion['lines'])} líneas de unión.")

    print("\n" + "=" * 50)
    print("¡TODAS LAS PRUEBAS UNITARIAS PASARON EXITOSAMENTE!")
    print("=" * 50)

if __name__ == "__main__":
    test_all()
