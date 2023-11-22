# Despliegue de modelos de IA en arquitecturas de microservicios


## Introducción
### Comprendiendo los microservicios
En el mundo del desarrollo de software, dos arquitecturas fundamentales han marcado el rumbo de cómo se estructuran las aplicaciones: los monolitos y los microservicios.

- Los monolitos encapsulan todas las funcionalidades de una aplicación en un bloque único. Son ideales cuando se quiere desarrollar aplicaciones sencillas de manera rápida, pero una de sus principales desventajas es que son costosos de escalar. El único escalado posible trabajando con monolitos es el vertical, donde para aumentar el rendimiento y capacidad de la aplicacion es necesario aumentar las especificaciones del servidor que la aloja. Si se necesita más RAM, se cambian las tarjetas de RAM por otras de mayor capacidad, si se necesita más capacidad de procesamiento, toca cambiar el procesador por otro de una gama más alta, etcétera. Esto puede salir muy caro conforme más y más gente hace uso de la app, ya que se necesita tecnología cada vez más punta para sostenerla.

- Este problema lo resuelven las arquitecturas de microservicios. En lugar de desplegar el software en una sola máquina, se dividen las funcionalidades que tiene en diferentes componentes modulares que pueden alojarse en máquinas independientes. De esta manera podemos tener por ejemplo una máquina encargada de autenticar usuarios, otra de realizar operaciones CRUD sobre la báse de datos y otra únicamente para alojar la base de datos en sí misma. Esto permite reducir costos ejecutando cada servicio en una máquina de gama baja y escalar solo aquellas que lo requieran, algo que se conoce como escalado horizontal. Otra de las ventajas de este enfoque es que se pueden delegar algunos servicios fácilmente a terceros. Por ejemplo, si queremos implementar un sistema de pagos en nuestra aplicación, a lo mejor nos conviene contratar un servicio como Stripe y olvidarnos de todos los dolores de cabeza que trae algo tan complejo y delicado como el tratamiento de datos bancarios. Simplemente conectamos nuestros servicios con su API, ¡y listo! Un enfoque arquitectónico en microservicios también posibilita dividir la _code base_ en multiples repositorios. Esto simplifica mucho los procesos de CI/CD, ya que cuando trabajamos sobre una funcionalidad, únicamente desplegamos en el servidor de esa funcionalidad y no interrumpimos ningún otro proceso de nuestra app. Las ventajas de usar microservicios son muchas, pero también aparecen nuevos retos que debemos resolver que hacen que este enfoque no sea el ideal en todos los casos. Pueden aprender más en detalle acerca de los microservicios en este enlace:

_[Mas información sobre los microservicios](https://www.youtube.com/watch?v=rv4LlmLmVWk&t)_

### Data science y microservicios
En una aplicación centrada en la IA, muchos de los recursos de un servidor se pueden ir en hacer predicciones con un modelo. ¿Y si os digo que podemos también encapsular toda funcionalidad de nuestro modelo en un único servicio desplegable de manera independiente? Pues bien, esto no solo podemos conseguirlo, sino que además es mucho más fácil de lo que probablemente se imaginan. En este contenido aprenderán a aprovechar al máximo las funcionalidades del potente y ágil framwork de desarrollo de APIs en Python, [FastAPI](https://fastapi.tiangolo.com/). Verán como con un simple script pueden agilizar su trabajo y el de sus compañeros proporcionándoles una forma fácil, segura e intuitiva de integrar modelos de inteligencia artificial en cualquier stack tecnológico.

Sin más dilación, ¡vamos allá!

## Prerequisitos
Antes que nada, vamos a crear un entorno virtual para trabajar. Esto es opcional, pero recomendado.

```sh
python -m venv venv
```

Para activar el entorno, ejecutamos el siguiente comando:

```sh
source venv/bin/activate # linux
. 'C:\<directorio del repo>\venv\Scripts\Activate.ps1' # powershell
```

Ahora podemos instalar FastAPI. Para ello utilizaremos el administrador de paquetes de Python:

```sh
pip install fastapi
```

Además de esto, vamos a necesitar Uvicorn para poder alojar nuestra API y Scikit Learn para poder utilizar el modelo que tenemos como ejemplo:

```sh
pip install uvicorn scikit-learn
```

Podemos crear nuestra primera API en un archivo `main.py` de la siguiente manera:

```py
from fastapi import FastAPI # importamos objeto FastAPI

app = FastAPI() # instancializamos una app

@app.get('/') # definimos el método HTTP y la ruta del endpoint
async def root(): # definimos la función que se debe ejecutar cuando se realiza una request a la ruta especificada con el método espcificado
    return {'Hola': 'Mundo'} # la respuesta que queremos retornar
```

Listo, ya tenemos una API. Podemos comprobar si todo funciona correctamente ejecutando el siguiente comando en nuestra terminal para desplegar el servidor de Uvicorn y yendo al puerto 8000 de localhost:

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Con `main:app` estamos indicandole a Uvicorn que la instancia que debe alojar es la que está guardada bajo la variable `app` en el fichero `main.py`. Con `--host 0.0.0.0` estamos declarando que el servidor se ha de ejecutar en el mismo ordenador en el que se ha ejecutado el comando. Por último definimos el puerto por el que podemos comunicarnos con el servidor utilizando `--port 8000` y marcamos `--reload` para que el servidor se reinicie cada vez que detecte algún cambio en nuestro código.

Una vez ejecutado el comando, podemos navegar utilizando nustro navegador preferido a http://localhost:8000/ y veremos una resupuesta que diga `{"Hola":"Mundo"}`.

## Pydantic
Uno de los puntos más fuertes de FastAPI en comparación con otros frameworks de desarrollo de APIs en Python es que está construido sobre Pydantic. Como muchos sabrán, Python es un lenguaje con tipado dinámico, esto quiere decir que cuando definimos alguna variable, no hace falta declarar el tipo de esa variable (si es una cadena, entero, flotante, etc.), sino que Python detecta automáticamente qué tipo es. Es más, podemos definir una variable `var = 42`, y más adelante en nuestro código darle un valor de un tipo completamente diferente: `var = "cuarenta y dos"`. Esto tiene sus cosas buenas, pero un problema que no podemos pasar por alto es que podemos encontrarnos con bugs completamente inesperados donde intentamos hacer acciones sobre una variable que creemos que es de un tipo, cuando en realidad la hemos sobreescrito con otro tipo en alguna parte de nuestro código sin darnos cuenta.

Pydantic resuelve este problema aprovechando la funcionalidad de Python de _type hinting_. Esta funcionalidad se introdujo en la versión 3.5 y nos permite especificar el tipo de las variables, parámetros y retornos. Si bien esto no afecta de ninguna manera a la funcionalidad del código, ya que podemos marcar una variable como cadena y Python no va a rechistar si esa variable recibe un entero, ayuda a los IDEs como PyCharm y VSCode a identificar bien las variables y ofrecer compleciones de código más acertadas. Lo que hace Pydantic es ofrecer un framework orientado a objetos en el que podemos imponer los tipos a las variables, de tal manera que si en algún momento se incumplen, obtenemos un error con el que podemos trabajar. En algunos casos, incluso castea automáticamente una variable al tipo deseado. Genial, ¿cómo podemos aprovechar esto? Pues simplemente importamos la clase BaseModel y creamos todas nuestras estructuras de datos heredando siempre a partir de esa clase:

```py
from pydantic import BaseModel

class Persona(BaseModel):
    edad: int
    nombre: str
    profesion: str
    estatura: float
    mascotas: list[str] = []
```
Como pueden ver, los tipos los definimos con dos puntos y a continuación el tipo. Podemos incluso inicializar algunos atributos con valores por defecto. Pero esto no es todo, también podemos usar otros modelos de pydantic como tipos. Aquí un ejemplo:

```py
from pydantic import BaseModel

class Mascota(BaseModel):
    edad: int
    nombre: str
    especie: str

class Persona(BaseModel):
    edad: int
    nombre: str
    profesion: str
    estatura: float
    mascotas: list[Mascota] = []
```

Incluso podemos utilizar enums que trae Python de forma nativa:

```py
from pydantic import BaseModel
from enum import Enum

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
```

Para usar alguna de estas clases, las instancializamos como cualquier otra clase con las que hayamos trabajado:

```py
mascota_1 = Mascota(edad=5, nombre="Garfield", especie=Especie.gato)
mascota_2 = Mascota(edad=3, nombre="Odie", especie=Especie.perro)
persona = Persona(edad=42, nombre="Benito Camelas", profesion="Senior Data Scientist", estatura=1.85, mascotas=[mascota_1, mascota_2])
```

Si hubiera algún error en los datos, como por ejemplo que la estatura fuese `"Lorem ipsum dolor sit amet"`, no pasaría desapercibido ya que obtendríamos una excepción.

Todo este sistema de validación de datos está genial, pero hay veces que necesitamos tener los datos en un formato más estandarizado como un diccionario para poder comunicarnos con otros programas. Al fin y al cabo, estamos trabajando con microservicios y buscamos serializar y deserializar nuestras estructuras a JSON. Bien, esto es tan simple como escribir:

```py
diccionario_persona = persona.model_dump()
```

Ahora, si guardamos el `diccionario_persona` como un archivo JSON, tendremos el siguiente contenido:
```json
{
    "edad": 42, 
    "nombre": "Benito Camelas", 
    "profesion": "Senior Data Scientist", 
    "estatura": 1.85, 
    "mascotas": 
    [
        {
            "edad": 5, 
            "nombre": "Garfield", 
            "especie": "Gato"
        }, 
        {
            "edad": 3, 
            "nombre": "Odie", 
            "especie": "Perro"
        }
    ]
}
```

## API

Ahora que hemos visto cómo trabajar con Pydantic, podemos proceder a desarrollar nuestra API. Para esto voy a utilizar un modelo RandomForestRegressor de Scikit Learn que ya está entrenado. Este modelo predice los precios de viviendas en Madrid y necesita una multitud de parámetros:
- Latitud
- Longitud
- Superficie construida
- Número de baños
- Número de habitaciones
- Si tiene o no un jardín
- Antigüedad de la vivienda
- Superficie útil
- Si tiene o no un ascensor
- Si tiene o no un garaje
- Condición de la vivienda

Con toda esta cantidad de variables, cada una de un tipo diferente, conviene tener un formato estandarizado que no de lugar a errores. A continuación pueden ver la implementación de los modelos de Pydantic para estructurar los datos que va a recibir el endpoint de nuestra API y la predicción que va a retornar.

```py
from enum import Enum
from pydantic import BaseModel

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
```

Ahora podemos crear el endpoint de nuestra API. Para poder recibir los datos, utilizaremos el método HTTP post. La gracia de que FastAPI esté construido sobre Pydantic es que podemos especificar nuestros modelos como parámetros de las funciones y FastAPI se encargará de deserializar la cadena JSON que recibimos y convertirla en ese modelo. De esta manera, estaremos validando los datos al recibirlos sin tener que hacer nada nosotros mismos. Tras la validación, podemos hacer .model_dump() y trabajar con los datos de la manera que nos sea más conveniente.

```py
@app.post('/predecir')
async def ruta_prediccion(formulario: Formulario) -> Prediccion:
    pass
```

Aquí ponemos en práctica un _type hint_ que no hemos visto anteriormente. Con `->` podemos señalar qué tipo de variable retornará la función, en este caso un modelo de pydantic que creamos llamado Prediccion.

Vamos a terminar de construir la función. Lo primero que debemos hacer es extraer los valores de los diferentes campos que tiene el formulario de la request. Tenemos que recordar que, para las predicciones, el modelo debe recibir los datos en el mismo orden en el que los fue recibiendo al entrenar. En nuestro caso, el orden es igual al orden en el que hemos declarado los campos del modelo en la clase Formulario. Partiendo de ahí, podemos construir una lista con los valores de cada campo respetando ese mismo orden. Para hacerlo utilizaremos la función nativa de Python `getattr(instance, field)` y la propiedad `BaseModel().model_fields`. La función `getattr()` recibe una instancia y un campo de una clase, y devuelve el valor de ese campo. Por otro lado, `BaseModel().model_fields` retorna un iterable con todos los campos de una clase en el mismo orden en el que se declararon. 

```py
@app.post('/predecir')
async def ruta_prediccion(formulario: Formulario) -> Prediccion:
    valores_ordenados = [getattr(formulario, campo) for campo in formulario.model_fields]
```

Ahora podemos cargar nuestro modelo:

```py
import pickle as pkl
from sklearn.ensemble import RandomForestRegressor

def cargar_modelo() -> RandomForestRegressor:
    with open('model.pkl', 'br') as file:
        modelo = pkl.load(file)
    return modelo
```

Vamos a hacer también una función para cargar los encodings que utilizaremos para convertir nuestro campo de condición a un valor numérico que el modelo entienda bien.

```py
def cargar_encodings() -> dict:
    with open('encodings.pkl', 'br') as file:
        encodings = pkl.load(file)
    return encodings
```

Volvemos a nuestra función de ruta y cargamos el modelo junto a los encodings:

```py
@app.post('/predecir')
async def ruta_prediccion(formulario: Formulario) -> Prediccion:
    valores_ordenados = [getattr(formulario, campo) for campo in formulario.model_fields]

    modelo = cargar_modelo()
    encodings = cargar_encodings()
```

Ahora podemos cambiar el valor de la condición por un valor numérico:

```py
@app.post('/predecir')
async def ruta_prediccion(formulario: Formulario) -> Prediccion:
    valores_ordenados = [getattr(formulario, campo) for campo in formulario.model_fields]

    modelo = cargar_modelo()
    encodings = cargar_encodings()

    valor_de_condicion = valores_ordenados[-1]
    valor_de_condicion_numerico = encodings['condicion'][valor_de_condicion]
    valores_ordenados[-1] = valor_de_condicion_numerico
```

Por fin podemos hacer la predicción. Hay que recordar que los modelos de Scikit Learn reciben matrices, por lo que nuestra lista de valores_ordenados debe ir envuelta en otra lista.

```py
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
```

Por último, vamos a sacar el timestamp de cuando se ha hecho la predicción y vamos a construir una instancia de Prediccion para retornarla:

```py
import datetime

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
```

Ya está listo nuestro endpoint. Ahora si hacemos una post request con los datos necesarios en formato JSON a http://localhost:8000/predecir, deberíamos obtener una respuesta con un código 200 y un JSON como este:

```json
{
    "precio": 158827.2,
    "timestamp": 1700660949.076112
}
```

Pueden probar todos sus endpoints a través del endpoint http://localhost:8000/docs que proporciona FastAPI. Ahí tendréis una documentación de vuestra API generada a partir de vuestro código. Si aprovechan bien todas las funcionalidades de FastAPI y Pydantic, esta documentación estará muy completa y cualquiera que use vuestra API puede navegarla y no solo entender como funcionan los endpoints, sino probarlos ellos mismos.

Podemos crear más endpoints, todos los que queramos. Por ejemplo, podemos tener uno para hacer predicciones en baches y otro para evaluar el modelo con un dataset de validación, pero esto lo dejo como ejercicio de práctica que deberán resolver por vuestra cuenta.

## Contenedorización
Si queremos desplegar nuestra API en la nube de una manera sencilla y sin preocuparnos por las dependencias, versiones y el entorno, una solución es utilizar Docker para encapsular nuestra API. Para ello, debemos tener Docker instalado en nuestro ordenador. Si estamos usando Windows, debemos tener ademas instalado el Linux Subsistem for Windows (LSW). Para instalar docker, pueden seguir las instrucciones de instalación en su [página web](https://docs.docker.com/engine/install/).

Una vez instalado, procedemos a crear una imágen con nuestra API. Para ello, creamos un archivo `Dockerfile` sin extensión y con la primera letra mayúscula. Dentro, vamos a definir lo que necesitamos para ejecutar correctamente la API. Para nuestro caso, vamos a utilizar el siguiente Dockerfile:

```Dockerfile
FROM python:3.10-alpine

WORKDIR /api

COPY ./requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev && \
    apk add --no-cache libffi-dev libressl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

RUN pip install uvicorn

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
```

Vamos a ir paso por paso para entender qué está pasando en este archivo. En primer lugar, estamos definiendo la imágen base con la palabra FROM. Esta imágen contiene todo lo necesario para construir un sistema operativo Alpine con Python 3.10 instalado:

```Dockerfile
FROM python:3.10-alpine
```

Podemos utilizar otros sistemas operativos y otras versiones de Python, todo lo que tenemos que hacer es explorar en [dockerhub]() las imágenes que nos interesen.

Lo siguiente que estamos definiendo es un directorio `/app`. Con el comando `WORKDIR` estamos creando ese directorio y estamos navegando hacia él para trabajar dentro. Esto es opcional para una imágen tan sencilla como esta, pero recomendable hacerlo siempre para tener buenas prácticas:

```Dockerfile
FROM python:3.10-alpine

WORKDIR /api
```

Ahora copiamos los contenidos del archivo `requirements.txt` que creamos antes a `.`, que es nuestro workdir:

```Dockerfile
FROM python:3.10-alpine

WORKDIR /api

COPY ./requirements.txt .
```

A continuación ejecutamos un comando para actualizar el sistema operativo, agregar dependencias temporales e instalar todas las librerías que tenemos en `requirements.txt`:

```Dockerfile
FROM python:3.10-alpine

WORKDIR /api

COPY ./requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev && \
    apk add --no-cache libffi-dev libressl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps
```

Ahora instalamos Uvicorn:

```Dockerfile
FROM python:3.10-alpine

WORKDIR /api

COPY ./requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev && \
    apk add --no-cache libffi-dev libressl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

RUN pip install uvicorn
```

Ahora que tenemos instaladas todas las dependencias, podemos copias los contenidos de nuestra API a la imágen:

```Dockerfile
FROM python:3.10-alpine

WORKDIR /api

COPY ./requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev && \
    apk add --no-cache libffi-dev libressl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

RUN pip install uvicorn

COPY . .
```

Si hay alguna carpeta o archivo que no queremos guardar en la imágen, por ejemplo nuestro entorno virtual `venv`, podemos añadirlos a un archivo `.dockerignrore`:

```.dockerignore
/venv/
__pycache__/
```

Una vez todo lo necesario está dentro de la imágen, abrimos el puerto 8000, que es por el que se comunica Uvicorn cuando ejecutamos nuestro servidor:

```Dockerfile
FROM python:3.10-alpine

WORKDIR /api

COPY ./requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev && \
    apk add --no-cache libffi-dev libressl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

RUN pip install uvicorn

COPY . .

EXPOSE 8000
```

Por último, especificamos el comando que se ha de ejecutar para iniciar el programa, en nuestro caso el servidor de Uvicorn:

```Dockerfile
FROM python:3.10-alpine

WORKDIR /api

COPY ./requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev && \
    apk add --no-cache libffi-dev libressl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

RUN pip install uvicorn

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
```

Para comprobar que todo funciona correctamente, debemos construir la imágen a partir de Dockerfile y luego instancializar un contenedor. La imágen se construye con el siguiente comando:

```sh
docker build -t api .
```

Donde `-t api` nos sirve para especificar el nombre de la imágen y el `.` especifica el directorio en el que se encuentra el Dockerfile.

Para instancializar un contenedor a partir de la imágen, ejecutamos:

```sh
docker run -p 8000:8000 api
```

Con `-p 8000:8000` estamos diciendo que vamos a enlazar el puerto 8000 del contenedor al puerto 8000 de nuestro ordenador. Esto nos permite comunicarnos con el contenedor de manera directa. Luego, `api` es simplemente el nombre de la imágen que hemos creado.

Si entramos a http://localhost:8000/, podremos ver nuestra API en funcionamiento. Y así, con un poco de esfuerzo, hemos convertido un modelo de Scikit Learn en un software que cualquier desarrollador puede integrar en su aplicación con mínimo esfuerzo. Veamos como podemos utilizarlo nosotros.

## Uso
Ahora, con el contenedor corriendo en nuestro ordenador, podemos utilizar la librería requests para utilizar la API. Acuérdense de instalarla, pues no es un módulo nativo de Python:

```sh
pip install requests
```

Digamos que estamos construyendo una aplicación de Streamlit en la que queremos aprovechar este modelo. Podemos pedir datos de la siguiente manera:

```py
import streamlit as st

def main():
    latitud = st.number_input("Latitud")
    longitud = st.number_input("Longitud")
    superficie_construida = st.number_input("Superficie Construida")
    baños = st.number_input("Baños")
    habitaciones = st.number_input("Habitaciones")
    jardin = st.checkbox("Jardín")
    antiguedad = st.number_input("Antigüedad")
    superficie_util = st.number_input("Superficie Útil")
    ascensor = st.checkbox("Ascensor")
    garaje = st.checkbox("Garaje")
    condicion = st.selectbox("Condición", options=['A estrenar', 'En buen estado', 'Reformado', 'A reformar'], index=0)

if __name__ == '__main__':
    main()
```

Y ahora podemos crear un botón para hacer una request con esos datos a http:localhost:8000/predecir, o a otro enlace si por ejemplo decidimos alojar el modelo en la nube.

```py
import streamlit as st

def main():
    latitud = st.number_input("Latitud")
    longitud = st.number_input("Longitud")
    superficie_construida = st.number_input("Superficie Construida")
    baños = st.number_input("Baños")
    habitaciones = st.number_input("Habitaciones")
    jardin = st.checkbox("Jardín")
    antiguedad = st.number_input("Antigüedad")
    superficie_util = st.number_input("Superficie Útil")
    ascensor = st.checkbox("Ascensor")
    garaje = st.checkbox("Garaje")
    condicion = st.selectbox("Condición", options=['A estrenar', 'En buen estado', 'Reformado', 'A reformar'], index=0)

    data = {
        "latitud" : latitud,
        "longitud" : longitud,
        "superficie_construida" : superficie_construida,
        "baños" : baños,
        "habitaciones" : habitaciones,
        "jardin" : jardin,
        "antiguedad" : antiguedad,
        "superficie_util" : superficie_util,
        "ascensor" : ascensor,
        "garaje" : garaje,
        "condicion" : condicion
    }

    endpoint = "http://localhost:8000/predecir"

    response = requests.post(url = endpoint, data = data)

    st.success(response.json())
    
if __name__ == '__main__':
    main()
```

Ahora tenemos dos repositorios separados, uno con el frontend en Streamlit, y otro con el backend utilizando FastAPI. Lo bueno de esto es que no estamos atados a Streamlit, ya que de la misma manera puede un desarrollador de React utilizar nuestra API en su página web y un desarrollador de Flutter en su aplicación Android. Ahora este modelo se puede integrar fácilmente en aplicaciones más complejas, donde por ejemplo solo ciertos usuarios que pagan una subscripción pueden utilizar este servicio. Las posibilidades son infinitas.