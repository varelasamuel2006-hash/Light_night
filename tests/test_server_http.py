import sys
import os
import time
import subprocess
import requests

def test_live_server():
    print("Iniciando servidor Uvicorn en segundo plano...")
    proc = subprocess.Popen(
        ["/home/samuel/mi_entorno_definitivo/bin/uvicorn", "server:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd="/home/samuel/mi_entorno_definitivo/Light_night/Light_night",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    base_url = "http://127.0.0.1:8000"
    server_ready = False

    # Esperar a que el servidor esté listo (hasta 10 segundos)
    for _ in range(20):
        try:
            r = requests.get(f"{base_url}/api/health", timeout=1)
            if r.status_code == 200 and r.json().get("status") == "ok":
                server_ready = True
                break
        except Exception:
            time.sleep(0.5)

    if not server_ready:
        proc.kill()
        raise RuntimeError("El servidor Uvicorn no respondió a tiempo.")

    print("✓ Servidor respondiendo en http://127.0.0.1:8000")

    try:
        # 1. Probar frontend estático (index.html)
        print("Probando GET / (Frontend estático)...")
        r_home = requests.get(base_url, timeout=3)
        assert r_home.status_code == 200
        assert "Light Night" in r_home.text
        assert "sky-canvas" in r_home.text
        print("✓ GET / sirve index.html correctamente.")

        # 2. Probar archivos estáticos CSS y JS
        print("Probando GET /css/style.css y /js/app.js...")
        r_css = requests.get(f"{base_url}/css/style.css", timeout=3)
        assert r_css.status_code == 200
        r_js = requests.get(f"{base_url}/js/app.js", timeout=3)
        assert r_js.status_code == 200
        print("✓ Archivos estáticos CSS y JS accesibles.")

        # 3. Probar API: Catálogo de constelaciones
        print("Probando GET /api/constellations...")
        r_consts = requests.get(f"{base_url}/api/constellations", timeout=3)
        assert r_consts.status_code == 200
        data_consts = r_consts.json()
        assert len(data_consts["constellations"]) >= 5
        print(f"✓ GET /api/constellations devolvió {len(data_consts['constellations'])} constelaciones.")

        # 4. Probar API: Geocodificación
        print("Probando POST /api/geocode...")
        r_geo = requests.post(f"{base_url}/api/geocode", json={"query": "Barcelona"}, timeout=5)
        assert r_geo.status_code == 200
        data_geo = r_geo.json()
        assert data_geo["success"] is True
        assert "latitude" in data_geo["data"]
        print(f"✓ POST /api/geocode encontró Barcelona en lat {data_geo['data']['latitude']}")

        # 5. Probar API: Cálculo astronómico (/api/sky)
        print("Probando POST /api/sky...")
        payload = {
            "latitude": 41.3879,
            "longitude": 2.16992,
            "min_altitude": 0,
            "constellation": None
        }
        r_sky = requests.post(f"{base_url}/api/sky", json=payload, timeout=5)
        assert r_sky.status_code == 200
        data_sky = r_sky.json()
        assert data_sky["status"] == "success"
        assert data_sky["total_visible_stars"] > 0
        print(f"✓ POST /api/sky calculó {data_sky['total_visible_stars']} estrellas visibles con éxito.")

        print("\n" + "=" * 55)
        print("¡TODAS LAS PRUEBAS DE INTEGRACIÓN HTTP FUNCIONARON!")
        print("=" * 55)

    finally:
        proc.terminate()
        proc.wait(timeout=3)
        print("Servidor detenido limpiamente.")

if __name__ == "__main__":
    test_live_server()
