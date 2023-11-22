from pydantic import BaseModel
from enum import Enum
from pprint import pprint
import json
class Especie(str, Enum):
    gato = 'Gato'
    perro = 'Perro'

class Mascota(BaseModel):
    edad: int
    nombre: str
    especie: Especie

class Persona(BaseModel):
    edad: int
    nombre: str
    profesion: str
    estatura: float
    mascotas: list[Mascota] = []

mascota_1 = Mascota(edad=5, nombre="Garfield", especie=Especie.gato)
mascota_2 = Mascota(edad=3, nombre="Odie", especie=Especie.perro)
persona = Persona(edad=42, nombre="Benito Camelas", profesion="Senior Data Scientist", estatura=1.85, mascotas=[mascota_1, mascota_2])

diccionario_persona = persona.model_dump()

with open('example.json', 'w') as file:
    json.dump(diccionario_persona, file)