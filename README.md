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

Una vez ejecutado el comando, podemos navegar utilizando nustro navegador preferido a [localhost](http://0.0.0.0:8000/) y veremos una resupuesta que diga {"Hola":"Mundo"}.
