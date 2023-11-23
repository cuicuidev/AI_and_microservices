from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.ensemble import RandomForestRegressor

from enum import Enum
import datetime
import pickle as pkl

class Condicion(str, Enum):
    a_reformar = 'A reformar'
    reformado = 'Reformado'
    a_estrenar = 'A estrenar'
    en_buen_estado = 'En buen estado'

class Formulario(BaseModel):
    latitud: float
    longitud: float
    superficie_construida: float
    baños: int
    habitaciones: int
    jardin: bool
    antiguedad: float
    superficie_util: float
    ascensor: bool
    garaje: bool
    condicion: Condicion

class Prediccion(BaseModel):
    precio: float
    timestamp: float

app = FastAPI()

@app.get('/')
async def root():
    return {'Hola': 'Mundo'}


def cargar_modelo() -> RandomForestRegressor:
    with open('model.pkl', 'br') as file:
        modelo = pkl.load(file)
    return modelo


def cargar_encodings() -> dict:
    with open('encodings.pkl', 'br') as file:
        encodings = pkl.load(file)
    return encodings


@app.post('/predecir')
async def ruta_prediccion(formulario: Formulario) -> Prediccion:
    valores_ordenados = [getattr(formulario, campo) for campo in formulario.model_fields]

    modelo = cargar_modelo()
    encodings = cargar_encodings()

    valor_de_condicion = valores_ordenados[-1]
    valor_de_condicion_numerico = encodings['condicion'][valor_de_condicion]
    valores_ordenados[-1] = valor_de_condicion_numerico

    precios = modelo.predict([valores_ordenados])
    precio = precios[0]

    timestamp = datetime.datetime.now().timestamp()
    prediccion = Prediccion(precio=precio, timestamp=timestamp)
    return prediccion

@app.get('/landing_page')
async def landing_page():
    with open('index.html') as file:
        land = file.read()
    return land