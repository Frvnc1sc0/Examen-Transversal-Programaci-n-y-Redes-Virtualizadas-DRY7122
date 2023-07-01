integrantes = [
    {"Nombre": "Francisco", "Apellido": "SanMartin"},
    {"Nombre": "Claudio", "Apellido": "Rivera"},
    {"Nombre": "Matias", "Apellido": "Codocedo"},
    {"Nombre": "Tomas", "Apellido": "Moyano"},
]

for integrantes in integrantes:
    nombre_completo = f"{integrantes['Nombre']} {integrantes['Apellido']}"
    print(nombre_completo)
