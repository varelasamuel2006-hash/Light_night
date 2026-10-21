"""
Catálogo astronómico de constelaciones y estrellas para Light_night.
Conserva 100% los datos y coordenadas del script original (Orion, Ursa Mayor, Cassiopeia, Leo, Scorpius)
y amplía el catálogo con más constelaciones prominentes, magnitudes visuales, colores y conexiones estelares.
"""

CONSTELLATIONS = {
    "orion": {
        "id": "orion",
        "name": "Orión",
        "latin_name": "Orion",
        "season": "Invierno (Hemisferio Norte)",
        "description": "El Cazador de la mitología griega. Alberga a Betelgeuse (supergigante roja) y Rigel (supergigante azul), con el inconfundible cinturón de tres estrellas alineadas (Alnitak, Alnilam y Mintaka).",
        "stars": [
            {"nombre": "Betelgeuse", "ra": 5.9195, "dec": 7.4071, "mag": 0.42, "color": "#ffaa77", "tipo": "Supergigante roja variable"},
            {"nombre": "Rigel", "ra": 5.2423, "dec": -8.2016, "mag": 0.13, "color": "#c2dcff", "tipo": "Supergigante azul-blanca"},
            {"nombre": "Bellatrix", "ra": 5.4189, "dec": 6.3497, "mag": 1.64, "color": "#c2dcff", "tipo": "Gigante azul"},
            {"nombre": "Alnitak", "ra": 5.6793, "dec": -1.9426, "mag": 1.77, "color": "#b5d5ff", "tipo": "Supergigante azul"},
            {"nombre": "Alnilam", "ra": 5.6036, "dec": -1.2019, "mag": 1.69, "color": "#b5d5ff", "tipo": "Supergigante azul"},
            {"nombre": "Mintaka", "ra": 5.5334, "dec": -0.2991, "mag": 2.23, "color": "#c2dcff", "tipo": "Gigante azul múltiple"},
            {"nombre": "Saiph", "ra": 5.7959, "dec": -9.6696, "mag": 2.07, "color": "#b5d5ff", "tipo": "Supergigante azul"}
        ],
        "conexiones": [
            ("Betelgeuse", "Bellatrix"),
            ("Bellatrix", "Alnilam"),
            ("Alnilam", "Alnitak"),
            ("Alnilam", "Rigel"),
            ("Betelgeuse", "Alnitak"),
            ("Alnitak", "Saiph"),
            ("Rigel", "Saiph"),
            ("Alnilam", "Mintaka"),
            ("Mintaka", "Bellatrix")
        ]
    },
    "ursa mayor": {
        "id": "ursa mayor",
        "name": "Osa Mayor",
        'latin_name': "Ursa Major",
        "season": "Circumpolar (Norte)",
        "description": "La Gran Osa o El Carro. Sus dos estrellas apuntadoras frontales (Merak y Dubhe) trazan una línea recta que señala directamente a Polaris (Estrella Polar).",
        "stars": [
            {"nombre": "Dubhe", "ra": 11.0621, "dec": 61.7508, "mag": 1.79, "color": "#ffd699", "tipo": "Gigante naranja"},
            {"nombre": "Merak", "ra": 11.0307, "dec": 56.3824, "mag": 2.37, "color": "#ffffff", "tipo": "Estrella blanca de secuencia principal"},
            {"nombre": "Phecda", "ra": 11.8972, "dec": 53.6948, "mag": 2.44, "color": "#ffffff", "tipo": "Estrella blanca"},
            {"nombre": "Megrez", "ra": 12.2570, "dec": 57.0326, "mag": 3.31, "color": "#ffffff", "tipo": "Estrella blanca"},
            {"nombre": "Alioth", "ra": 12.9005, "dec": 55.9598, "mag": 1.77, "color": "#ffffff", "tipo": "Subgigante blanca brillante"},
            {"nombre": "Mizar", "ra": 13.3987, "dec": 54.9254, "mag": 2.23, "color": "#ffffff", "tipo": "Sistema estelar cuádruple"},
            {"nombre": "Alkaid", "ra": 13.7923, "dec": 49.3133, "mag": 1.86, "color": "#c2dcff", "tipo": "Estrella azul de secuencia principal"}
        ],
        "conexiones": [
            ("Dubhe", "Merak"),
            ("Merak", "Phecda"),
            ("Phecda", "Megrez"),
            ("Megrez", "Dubhe"),
            ("Megrez", "Alioth"),
            ("Alioth", "Mizar"),
            ("Mizar", "Alkaid")
        ]
    },
    "cassiopeia": {
        "id": "cassiopeia",
        "name": "Casiopea",
        "latin_name": "Cassiopeia",
        "season": "Otoño / Circumpolar",
        "description": "La reina vanidosa de Etiopía. Reconocible al instante por su silueta en forma de W o M en el cielo del norte, opuesta a la Osa Mayor respecto a Polaris.",
        "stars": [
            {"nombre": "Schedar", "ra": 0.6751, "dec": 56.5373, "mag": 2.24, "color": "#ffd699", "tipo": "Gigante naranja"},
            {"nombre": "Caph", "ra": 0.1528, "dec": 59.1498, "mag": 2.28, "color": "#fff4e8", "tipo": "Subgigante blanco-amarilla"},
            {"nombre": "Gamma Cas", "ra": 0.9451, "dec": 60.7167, "mag": 2.15, "color": "#c2dcff", "tipo": "Variable eruptiva azul"},
            {"nombre": "Ruchbah", "ra": 1.4302, "dec": 60.2353, "mag": 2.68, "color": "#ffffff", "tipo": "Binaria eclipsante blanca"},
            {"nombre": "Segin", "ra": 1.9066, "dec": 63.6701, "mag": 3.37, "color": "#c2dcff", "tipo": "Gigante azul"}
        ],
        "conexiones": [
            ("Caph", "Schedar"),
            ("Schedar", "Gamma Cas"),
            ("Gamma Cas", "Ruchbah"),
            ("Ruchbah", "Segin")
        ]
    },
    "leo": {
        "id": "leo",
        "name": "Leo",
        "latin_name": "Leo",
        "season": "Primavera",
        "description": "El León de Nemea derrotado por Hércules. Constelación zodiacal destacada que contiene el asterismo de 'La Hoz' y la estrella real Regulus.",
        "stars": [
            {"nombre": "Regulus", "ra": 10.1395, "dec": 11.9672, "mag": 1.35, "color": "#c2dcff", "tipo": "Sistema cuádruple azul-blanco"},
            {"nombre": "Denebola", "ra": 11.8177, "dec": 14.5720, "mag": 2.14, "color": "#ffffff", "tipo": "Estrella blanca (Cola del León)"},
            {"nombre": "Algieba", "ra": 10.3329, "dec": 19.8419, "mag": 2.08, "color": "#ffe099", "tipo": "Doble gigante dorada"},
            {"nombre": "Zosma", "ra": 11.2351, "dec": 20.5237, "mag": 2.56, "color": "#ffffff", "tipo": "Estrella blanca"},
            {"nombre": "Adhafera", "ra": 10.2809, "dec": 23.4173, "mag": 3.44, "color": "#fff4e8", "tipo": "Gigante blanca"},
            {"nombre": "Chertan", "ra": 11.2350, "dec": 15.4294, "mag": 3.32, "color": "#ffffff", "tipo": "Estrella blanca"}
        ],
        "conexiones": [
            ("Regulus", "Algieba"),
            ("Algieba", "Adhafera"),
            ("Algieba", "Zosma"),
            ("Zosma", "Chertan"),
            ("Chertan", "Denebola"),
            ("Zosma", "Denebola"),
            ("Regulus", "Chertan")
        ]
    },
    "scorpius": {
        "id": "scorpius",
        "name": "Escorpio",
        "latin_name": "Scorpius",
        "season": "Verano",
        "description": "El Escorpión que picó a Orión. Brilla en el cielo estival austral con su rojo corazón estelar Antares y una cola con aguijón que se curva hacia el centro galáctico.",
        "stars": [
            {"nombre": "Antares", "ra": 16.4901, "dec": -26.4320, "mag": 1.06, "color": "#ff7e54", "tipo": "Supergigante roja masiva"},
            {"nombre": "Shaula", "ra": 17.5600, "dec": -37.1038, "mag": 1.62, "color": "#c2dcff", "tipo": "Subgigante azul múltiple (El Aguijón)"},
            {"nombre": "Sargas", "ra": 17.6217, "dec": -42.9978, "mag": 1.86, "color": "#fff4e8", "tipo": "Gigante brillante blanca"},
            {"nombre": "Dschubba", "ra": 16.0056, "dec": -22.6217, "mag": 2.32, "color": "#c2dcff", "tipo": "Subgigante azul"},
            {"nombre": "Graffias", "ra": 16.0906, "dec": -19.8055, "mag": 2.62, "color": "#c2dcff", "tipo": "Sistema binario azul"}
        ],
        "conexiones": [
            ("Graffias", "Dschubba"),
            ("Dschubba", "Antares"),
            ("Antares", "Sargas"),
            ("Sargas", "Shaula")
        ]
    },
    "cygnus": {
        "id": "cygnus",
        "name": "Cisne",
        "latin_name": "Cygnus",
        "season": "Verano / Otoño",
        "description": "Conocida como la Cruz del Norte. Vuela hacia el sur a lo largo de la Vía Láctea estival con la supergigante Deneb en su cola y Albireo en la cabeza.",
        "stars": [
            {"nombre": "Deneb", "ra": 20.6905, "dec": 45.2803, "mag": 1.25, "color": "#ffffff", "tipo": "Supergigante blanca"},
            {"nombre": "Albireo", "ra": 19.5126, "dec": 27.9596, "mag": 3.08, "color": "#ffe099", "tipo": "Estrella doble de contrastes dorado y zafiro"},
            {"nombre": "Sadr", "ra": 20.3731, "dec": 40.2567, "mag": 2.23, "color": "#fff4e8", "tipo": "Supergigante blanco-amarilla"},
            {"nombre": "Gienah", "ra": 20.7699, "dec": 33.9703, "mag": 2.48, "color": "#ffd699", "tipo": "Gigante naranja"},
            {"nombre": "Fawaris", "ra": 19.6108, "dec": 45.1306, "mag": 2.87, "color": "#c2dcff", "tipo": "Gigante azul"}
        ],
        "conexiones": [
            ("Deneb", "Sadr"),
            ("Sadr", "Albireo"),
            ("Fawaris", "Sadr"),
            ("Sadr", "Gienah")
        ]
    },
    "lyra": {
        "id": "lyra",
        "name": "Lira",
        "latin_name": "Lyra",
        "season": "Verano",
        "description": "La Lira celestial de Orfeo. Contiene a Vega, la quinta estrella más luminosa del cielo y vértice principal del Triángulo de Verano.",
        "stars": [
            {"nombre": "Vega", "ra": 18.6156, "dec": 38.7836, "mag": 0.03, "color": "#cce3ff", "tipo": "Estrella blanca de secuencia principal"},
            {"nombre": "Sheliak", "ra": 18.8344, "dec": 33.3627, "mag": 3.52, "color": "#c2dcff", "tipo": "Variable eclipsante prototípica"},
            {"nombre": "Sulafat", "ra": 18.9814, "dec": 32.6900, "mag": 3.25, "color": "#c2dcff", "tipo": "Gigante azul brillante"},
            {"nombre": "Delta Lyrae", "ra": 18.9056, "dec": 36.9022, "mag": 4.30, "color": "#ffaa77", "tipo": "Gigante roja"},
            {"nombre": "Zeta Lyrae", "ra": 18.7467, "dec": 37.6044, "mag": 4.34, "color": "#ffffff", "tipo": "Binaria espectroscópica blanca"}
        ],
        "conexiones": [
            ("Vega", "Zeta Lyrae"),
            ("Zeta Lyrae", "Delta Lyrae"),
            ("Delta Lyrae", "Sulafat"),
            ("Sulafat", "Sheliak"),
            ("Sheliak", "Zeta Lyrae"),
            ("Vega", "Sheliak")
        ]
    },
    "canis major": {
        "id": "canis major",
        "name": "Can Mayor",
        "latin_name": "Canis Major",
        "season": "Invierno",
        "description": "El fiel perro cazador de Orión. Alberga a Sirio, la estrella individual más resplandeciente del firmamento nocturno.",
        "stars": [
            {"nombre": "Sirio", "ra": 6.7525, "dec": -16.7161, "mag": -1.46, "color": "#e8f2ff", "tipo": "Estrella blanca ultra brillante con enana blanca compañera"},
            {"nombre": "Adhara", "ra": 6.9771, "dec": -28.9721, "mag": 1.50, "color": "#c2dcff", "tipo": "Gigante azul luminosa"},
            {"nombre": "Wezen", "ra": 7.1398, "dec": -26.3932, "mag": 1.83, "color": "#fff4e8", "tipo": "Supergigante amarilla"},
            {"nombre": "Mirzam", "ra": 6.3783, "dec": -17.9559, "mag": 1.98, "color": "#c2dcff", "tipo": "Gigante azul variable"},
            {"nombre": "Aludra", "ra": 7.4015, "dec": -29.3031, "mag": 2.45, "color": "#c2dcff", "tipo": "Supergigante azul"}
        ],
        "conexiones": [
            ("Mirzam", "Sirio"),
            ("Sirio", "Wezen"),
            ("Wezen", "Adhara"),
            ("Wezen", "Aludra")
        ]
    },
    "taurus": {
        "id": "taurus",
        "name": "Tauro",
        "latin_name": "Taurus",
        "season": "Otoño / Invierno",
        "description": "El Toro celestial, cruzado por el legendario cúmulo de las Pléyades y presidido por Aldebarán, el ojo anaranjado y fiero del toro.",
        "stars": [
            {"nombre": "Aldebaran", "ra": 4.5987, "dec": 16.5093, "mag": 0.85, "color": "#ff9f55", "tipo": "Gigante naranja luminosa"},
            {"nombre": "Elnath", "ra": 5.4382, "dec": 28.6075, "mag": 1.65, "color": "#c2dcff", "tipo": "Gigante azul-blanca"},
            {"nombre": "Alcyone", "ra": 3.7900, "dec": 24.1051, "mag": 2.87, "color": "#c2dcff", "tipo": "Estrella más brillante de las Pléyades"},
            {"nombre": "Tianguan", "ra": 5.6274, "dec": 21.1426, "mag": 3.00, "color": "#c2dcff", "tipo": "Subgigante azul Be"},
            {"nombre": "Ain", "ra": 4.4770, "dec": 15.9617, "mag": 3.53, "color": "#ffe099", "tipo": "Gigante amarilla de las Híades"}
        ],
        "conexiones": [
            ("Alcyone", "Ain"),
            ("Ain", "Aldebaran"),
            ("Aldebaran", "Tianguan"),
            ("Ain", "Elnath"),
            ("Aldebaran", "Elnath")
        ]
    },
    "ursa minor": {
        "id": "ursa minor",
        "name": "Osa Menor",
        "latin_name": "Ursa Minor",
        "season": "Circumpolar (Norte)",
        "description": "El eje del cielo boreal. Su estrella principal, Polaris (la Estrella Polar), permanece casi inmóvil en el polo norte celeste mientras el resto de la bóveda gira a su alrededor.",
        "stars": [
            {"nombre": "Polaris", "ra": 2.5303, "dec": 89.2641, "mag": 1.98, "color": "#fff8e7", "tipo": "Supergigante cefeida (Estrella Polar)"},
            {"nombre": "Kochab", "ra": 14.8451, "dec": 74.1555, "mag": 2.07, "color": "#ffd699", "tipo": "Gigante naranja"},
            {"nombre": "Pherkad", "ra": 15.3460, "dec": 71.8340, "mag": 3.00, "color": "#ffffff", "tipo": "Gigante blanca"},
            {"nombre": "Yildun", "ra": 17.5367, "dec": 86.5863, "mag": 4.35, "color": "#ffffff", "tipo": "Estrella blanca"}
        ],
        "conexiones": [
            ("Polaris", "Yildun"),
            ("Yildun", "Pherkad"),
            ("Pherkad", "Kochab")
        ]
    },
    "gemini": {
        "id": "gemini",
        "name": "Géminis",
        "latin_name": "Gemini",
        "season": "Invierno",
        "description": "Los Gemelos celestiales Cástor y Pólux, hijos de Leda. Sus dos cabezas estelares brillan cerca del límite oriental de Orión.",
        "stars": [
            {"nombre": "Pollux", "ra": 7.7553, "dec": 28.0262, "mag": 1.14, "color": "#ffd699", "tipo": "Gigante naranja con exoplaneta confirmado"},
            {"nombre": "Castor", "ra": 7.5767, "dec": 31.8883, "mag": 1.58, "color": "#ffffff", "tipo": "Fascinante sistema séxtuple de estrellas"},
            {"nombre": "Alhena", "ra": 6.6285, "dec": 16.3992, "mag": 1.93, "color": "#ffffff", "tipo": "Subgigante blanca"},
            {"nombre": "Wasat", "ra": 7.3353, "dec": 21.9822, "mag": 3.53, "color": "#ffffff", "tipo": "Subgigante blanca múltiple"},
            {"nombre": "Mebsuta", "ra": 6.7328, "dec": 25.1311, "mag": 3.06, "color": "#ffe099", "tipo": "Supergigante amarilla"}
        ],
        "conexiones": [
            ("Castor", "Pollux"),
            ("Castor", "Mebsuta"),
            ("Pollux", "Wasat"),
            ("Mebsuta", "Alhena"),
            ("Wasat", "Alhena")
        ]
    },
    "bootes": {
        "id": "bootes",
        "name": "Boyero",
        "latin_name": "Bootes",
        "season": "Primavera / Verano",
        "description": "El Pastor de bueyes celestiales. Alberga a Arturo (Arcturus), una gigante roja-anaranjada resplandeciente, cuarta estrella más brillante del cielo.",
        "stars": [
            {"nombre": "Arcturus", "ra": 14.2610, "dec": 19.1822, "mag": -0.05, "color": "#ff9f55", "tipo": "Gigante naranja muy luminosa"},
            {"nombre": "Nekkar", "ra": 15.0319, "dec": 40.3908, "mag": 3.49, "color": "#ffd699", "tipo": "Gigante amarilla"},
            {"nombre": "Seginus", "ra": 14.5342, "dec": 38.3083, "mag": 3.04, "color": "#ffffff", "tipo": "Variable blanca Delta Scuti"},
            {"nombre": "Izar", "ra": 14.7497, "dec": 27.0742, "mag": 2.35, "color": "#ffe099", "tipo": "Binaria brillante dorada y azul"},
            {"nombre": "Muphrid", "ra": 13.9117, "dec": 18.3978, "mag": 2.68, "color": "#fff4e8", "tipo": "Subgigante amarilla"}
        ],
        "conexiones": [
            ("Arcturus", "Muphrid"),
            ("Arcturus", "Izar"),
            ("Izar", "Seginus"),
            ("Seginus", "Nekkar"),
            ("Nekkar", "Izar")
        ]
    }
}

# Estrellas de referencia y fondo celeste destacadas
BRIGHT_NAVIGATIONAL_STARS = [
    {"nombre": "Capella", "constelacion": "Auriga", "ra": 5.2781, "dec": 45.9980, "mag": 0.08, "color": "#ffe099", "tipo": "Gigante amarilla cuádruple"},
    {"nombre": "Procyon", "constelacion": "Canis Minor", "ra": 7.6550, "dec": 5.2250, "mag": 0.38, "color": "#fff8e7", "tipo": "Subgigante blanco-amarilla"},
    {"nombre": "Altair", "constelacion": "Aquila", "ra": 19.8464, "dec": 8.8683, "mag": 0.77, "color": "#ffffff", "tipo": "Estrella blanca de rotación ultrarrápida"},
    {"nombre": "Spica", "constelacion": "Virgo", "ra": 13.4199, "dec": -11.1613, "mag": 0.98, "color": "#c2dcff", "tipo": "Binaria masiva azul"},
    {"nombre": "Fomalhaut", "constelacion": "Piscis Austrinus", "ra": 22.9608, "dec": -29.6222, "mag": 1.17, "color": "#ffffff", "tipo": "Estrella blanca con disco de escombros planetario"}
]


def get_all_constellations_summary():
    """Devuelve un resumen de todas las constelaciones para selectores e índices."""
    return [
        {
            "id": c["id"],
            "name": c["name"],
            "latin_name": c["latin_name"],
            "season": c["season"],
            "description": c["description"],
            "star_count": len(c["stars"])
        }
        for c in CONSTELLATIONS.values()
    ]


def get_constellation_by_id(const_id: str):
    """Busca una constelación por su identificador normalizado."""
    return CONSTELLATIONS.get(const_id.strip().lower())
