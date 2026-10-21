from skyfield.api import Loader, Topos, Star
import os
from geopy.geocoders import Nominatim
import folium
import matplotlib.pyplot as plt

geolocator = Nominatim(user_agent="astro_app")

lugar = input("Introduce ciudad o pueblo: ")
location = geolocator.geocode(lugar)
if location is None:
    print("No se encontró la ubicación")
    exit()

lat = location.latitude
lon = location.longitude

ruta = os.path.expanduser('~/skyfield_data')
load = Loader(ruta)

ts = load.timescale()
eph = load('de421.bsp')



# Definir la ubicación del usuario en skyfield
ubicacion = Topos(latitude_degrees=lat, longitude_degrees=lon)

# coordenadas constelaciones 

constelaciones = {
    "orion": [
        ("Betelgeuse", 5.9195, 7.4071),
        ("Rigel", 5.2423, -8.2016),
        ("Bellatrix", 5.4189, 6.3497),
        ("Alnitak", 5.6793, -1.9426),
        ("Alnilam", 5.6036, -1.2019)
    ],
    "ursa mayor": [
        ("Dubhe", 11.0621, 61.7508),
        ("Merak", 11.0307, 56.3824),
        ("Phecda", 11.8972, 53.6948),
        ("Megrez", 12.2570, 57.0326),
        ("Alioth", 12.9005, 55.9598)
    ],
    "cassiopeia": [
        ("Schedar", 0.6751, 56.5373),
        ("Caph", 0.1528, 59.1498),
        ("Gamma Cas", 0.9451, 60.7167),
        ("Ruchbah", 1.4302, 60.2353),
        ("Segin", 1.9066, 63.6701)
    ],
    "leo": [
        ("Regulus", 10.1395, 11.9672),
        ("Denebola", 11.8177, 14.5720),
        ("Algieba", 10.3329, 19.8419),
        ("Zosma", 11.2351, 20.5237),
        ("Adhafera", 10.2809, 23.4173)
    ],
    "scorpius": [
        ("Antares", 16.4901, -26.4320),
        ("Shaula", 17.5600, -37.1038),
        ("Sargas", 17.6217, -42.9978),
        ("Dschubba", 16.0056, -22.6217),
        ("Graffias", 16.0906, -19.8055)
    ]
}

conexiones = {
    "orion": [
        ("Betelgeuse", "Bellatrix"),
        ("Bellatrix", "Alnilam"),
        ("Alnilam", "Alnitak"),
        ("Alnilam", "Rigel")
        ]
}

# Encontrar constelacion seleccionada

constelacion = input("Constelación: ").strip().lower()

estrellas = constelaciones.get(constelacion)

if not estrellas:
    print("Constelación no encontrada")
    exit()

# tiempo actual
t = ts.now()

# ubicar la estrella en el mapa

earth = eph['earth']
observador = earth + ubicacion

resultados = []

for nombre, ra, dec in estrellas:
    star = Star(ra_hours=ra, dec_degrees=dec)

    astrometric = observador.at(t).observe(star)
    apparent = astrometric.apparent()
    alt, az, _ = apparent.altaz()

    resultados.append({
        "nombre": nombre,
        "alt": alt.degrees,
        "az": az.degrees
    })

visibles = [e for e in resultados if e["alt"] > 5]
#visibles = resultados # Importante quitarlo al terminar el programa
#visibles = [e for e in resultados if e["alt"] > 0]

visibles.sort(key=lambda x: x["alt"], reverse=True)

if not visibles:
    print("\n❌ No hay estrellas visibles en esta constelación ahora mismo")
    exit()
else:
    print(f"\n🌌 Estrellas visibles: {constelacion.capitalize()}\n")

    #for estrella in visibles:
        #print(estrella["nombre"])
        #print("Altitud:", estrella["alt"])
        #print("Azimut:", estrella["az"])
        #print("-----")


# MAPA A ESCALA

x = [e["az"] for e in visibles]
y = [e["alt"] for e in visibles]
nombres = [e["nombre"] for e in visibles]

plt.style.use('dark_background')
plt.grid(False)
plt.close('all')
plt.figure()

sizes = [10 for _ in visibles]

plt.scatter(x, y, s=sizes)

for i, nombre in enumerate(nombres):
    plt.text(x[i], y[i], nombre)

for origen, destino in conexiones.get(constelacion, []):
    e1 = next((e for e in visibles if e["nombre"] == origen), None)
    e2 = next((e for e in visibles if e["nombre"] == destino), None)

    if e1 and e2:
        plt.plot([e1["az"], e2["az"]], [e1["alt"], e2["alt"]])

plt.gca().invert_xaxis()
plt.axhline(0, color="white", linewidth=1)
plt.xticks([0, 90, 180, 270, 360], ["N", "E", "S", "W", "N"])
plt.ylim(0, max(y) + 10)
plt.xlabel("Azimut")
plt.ylabel("Altitud")
plt.title(f"Cielo - {constelacion}")

plt.show()

