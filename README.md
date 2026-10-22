# Light_night 🌌✨ --> Web: https://lightnight.onrender.com/?utm_source=chatgpt.com

**Light_night** es una aplicación interactiva que permite visualizar en tiempo real las constelaciones y estrellas del firmamento nocturno en función de la ubicación geográfica del usuario y la fecha y hora seleccionadas.

---

## 🌟 Características Principales

- **Bóveda Celeste Interactiva:** Renderizado en Canvas con proyección azimutal cenital (el centro es el Cénit y el perímetro exterior es el horizonte con los cuatro puntos cardinales).
- **Navegación Fluida:** Soporte para arrastrar (pan), acercar/alejar (zoom) y centrar la vista.
- **Geolocalización Automática y Búsqueda Manual:**
  - Detección de ubicación mediante GPS del navegador (con solicitud de permiso y manejo amigable en caso de rechazo).
  - Búsqueda manual de cualquier ciudad o pueblo del mundo con geocodificación mediante `geopy` / Nominatim.
- **Control Temporal (Time Travel):**
  - Modo en vivo (tiempo real con auto-sincronización).
  - Selector de fecha y hora arbitraria.
  - Botones rápidos de avance y retroceso (-1d, -1h, +1h, +1d) para observar el movimiento de la bóveda celeste.
- **Interacción y Ficha Astronómica:** Haz clic sobre cualquier estrella o constelación para consultar su altitud, azimut, magnitud aparente, ascensión recta (RA), declinación (Dec), tipo espectral y datos mitológicos.
- **Capas Visuales Conmutables:** Activa o desactiva líneas de unión, nombres de estrellas, nombres de constelaciones, cuadrícula Alt/Az y filtro de ángulo sobre el horizonte.
- **Compatibilidad Total:** El script original de terminal (`Light_night_main.py` con Matplotlib) sigue funcionando al 100%.

---

## 🚀 Cómo Iniciar la Aplicación Web

### 1. Activar el entorno virtual

Si estás en WSL / Linux:
```bash
source /home/samuel/mi_entorno_definitivo/bin/activate
```

O instala las dependencias en tu entorno activo:
```bash
pip install -r requirements.txt
```

### 2. Iniciar el servidor web FastAPI

Desde la carpeta del proyecto:
```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
O directamente con Python:
```bash
python server.py
```

### 3. Abrir la aplicación en tu navegador

Abre tu navegador habitual (Chrome, Firefox, Edge, etc.) y visita:
```
http://localhost:8000
```

También puedes explorar la documentación interactiva de la API en:
```
http://localhost:8000/docs
```

---

## 🧪 Ejecución de Pruebas

Para validar los cálculos astronómicos y el servidor HTTP:

```bash
# Pruebas unitarias del motor astronómico y catálogo
python tests/test_core.py

# Pruebas de integración de la API REST
python tests/test_server_http.py
```

---

## 📁 Estructura del Proyecto

```
Light_night/
├── core/                       # Capa lógica y cálculo astronómico
│   ├── __init__.py
│   ├── astronomy.py           # Motor astronómico (Skyfield + Topos + de421.bsp)
│   ├── celestial_catalog.py   # Catálogo de estrellas, constelaciones y mitología
│   └── geocoding.py           # Servicio de geocodificación con Geopy / Nominatim
├── static/                     # Frontend de la aplicación web
│   ├── index.html             # Interfaz semántica responsive
│   ├── css/
│   │   └── style.css          # Diseño astronómico dark, glassmorphism y animaciones
│   └── js/
│       ├── sky_renderer.js    # Motor gráfico de renderizado del cielo en Canvas
│       └── app.js             # Controlador de estado, API, GPS y eventos
├── tests/                      # Suite de pruebas automatizadas
│   ├── test_core.py
│   └── test_server_http.py
├── server.py                   # Servidor FastAPI y endpoints REST
├── Light_night_main.py         # Script CLI original con visualización en Matplotlib
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Documentación del proyecto
```
