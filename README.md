# Despliegue de modelos de IA en arquitecturas de microservicios


## Introducción
### Comprendiendo los microservicios
En el mundo del desarrollo de software, dos arquitecturas fundamentales han marcado el rumbo de cómo se estructuran las aplicaciones: los monolitos y los microservicios.

- Los monolitos encapsulan todas las funcionalidades de una aplicación en un bloque único. Son ideales cuando se quiere desarrollar aplicaciones sencillas de manera rápida, pero su principal desventaja es que son costosos de escalar. El único escalado posible trabajando con monolitos es el vertical, donde para aumentar el rendimiento y capacidad de la aplicacion es necesario aumentar las especificaciones del servidor que la aloja. Si se necesita más RAM, se cambian las tarjetas de RAM por otras de mayor capacidad, si se necesita más capacidad de procesamiento, toca cambiar el procesador por otro de una gama más alta, etcétera. Esto puede salir muy caro conforme más y más gente hace uso de la app, ya que se necesita tecnología cada vez más punta para sostenerla.

- Este problema lo resuelven las arquitecturas de microservicios. En lugar de desplegar el software en una sola máquina, se dividen las funcionalidades que tiene en diferentes componentes modulares que pueden alojarse en máquinas independientes. De esta manera podemos tener por ejemplo una máquina encargada de autenticar usuarios, otra de realizar operaciones CRUD sobre la báse de datos y otra únicamente aloja la base de datos en sí. Esto permite reducir costos ejecutando cada servicio en una máquina de gama baja y escalar solo aquellas que lo requieran, algo que se conoce como escalado horizontal. Otra de las ventajas de este enfoque es que se pueden delegar algunos servicios fácilmente a terceros. Por ejemplo, si queremos implementar un sistema de pagos en nuestra aplicación, a lo mejor nos conviene contratar un servicio como Stripe y olvidarnos de todos los dolores de cabeza que trae algo tan complejo y delicado como el tratamiento de datos bancarios. Simplemente conectamos nuestros servicios con su API, ¡y listo!

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

Una vez ejecutado el comando, podemos navegar utilizando nustro navegador preferido a [localhost](http://0.0.0.0:8000/) y veremos una resupuesta que diga `{"Hola":"Mundo"}`.

## Pydantic
Uno de los puntos más fuertes de FastAPI en comparación con otros frameworks de desarrollo de APIs en Python es que está construido sobre Pydantic. Como muchos sabrán, Python es un lenguaje con tipado dinámico, esto quiere decir que cuando definimos alguna variable, no hace falta declarar el tipo de esa variable (si es una cadena, entero, flotante, etc.), sino que Python detecta automáticamente qué tipo es. Es más, podemos definir una variable `var = 42`, y más adelante en nuestro código darle un valor de un tipo completamente diferente: `var = "cuarenta y dos"`. Esto tiene sus cosas buenas, pero un problema que no podemos pasar por alto es que podemos encontrarnos con bugs completamente inesperados.

Pydantic resuelve este problema aprovechando la funcionalidad de Python de _type hinting_. Esta funcionalidad se introdujo en la versión 3.5 y nos permite especificar el tipo de las variables, parámetros y retornos. Si bien esto no afecta de ninguna manera a la funcionalidad del código, ya que podemos marcar una variable como cadena y Python no va a rechistar si esa variable recibe un entero, ayuda a los IDEs como PyCharm y VSCode a identificar bien las variables y ofrecer compleciones de código más acertadas. Sin embargo, Pydantic aprovecha esta funcionalidad y ofrece un framework orientado a objetos en el que podemos imponer los tipos a las variables, de tal manera que si en algún momento se incumplen, obtenemos un error con el que podemos trabajar. En algunos casos, incluso castea automáticamente una variable al tipo deseado. Genial, ¿cómo podemos aprovechar esto? Pues simplemente importamos la clase BaseModel y creamos todas nuestras estructuras de datos heredando siempre a partir de esa clase:

```py
from pydantic import BaseModel

class Persona(BaseModel):
    edad: int
    nombre: str
    profesion: str
    estatura: float
    mascotas: list[str]
```
Como pueden ver, los tipos los definimos con dos puntos y el tipo. Pero esto no es todo, también podemos usar otros modelos de pydantic como tipos. Aquí un ejemplo:

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
    mascotas: list[Mascota]
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
    mascotas: list[Mascota]
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
diccionario_persona = persona.dump_model()
```

Ahora bajo la variable `diccionario_persona` tenemos un diccionario de Python que se ve tal que así:
```json
{
    "edad": 42,
    "nombre": "Benito Camelas",
    "profesion": "Senior Data Scientist",
    "estatura": 1.85,
    "mascotas": [
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