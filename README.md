# motosAPI
Proyecto FastAPI desplegado en Render.
 
# Despliegue de MotosAPI en Render

## 1. Descripción del proyecto

**MotosAPI** es una aplicación desarrollada con **FastAPI** que permite la gestión de motos mediante:
- Una API REST
- Páginas web renderizadas con **Jinja2**
- Persistencia de datos usando **SQLModel**
- Base de datos **PostgreSQL**

La aplicación se despliega en la nube utilizando **Render**.

---

## 2. Estructura del proyecto

MotosAPI/
│── src/
│   ├── data/
│   │    └── db.py
│   ├── models/
│   │    └── motos.py
│   ├── static/
│   │    ├── images/
│   │    │    └── favicorn2.ico
│   │    └── styles.css
│   ├── templates/
│   │    ├── fragments/
│   │    │    └── base.html
│   │    ├── crear_moto.html
│   │    ├── editar_moto.html
│   │    ├── eliminar_moto.html
│   │    ├── index.html
│   │    ├── moto_detalle.html
│   │    └── motos.html
│   └── main.py
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── .gitignore


# 3. Preparación del repositorio GitHub

Crear un repositorio en GitHub

Subir los siguientes archivos y carpetas:

src/

Dockerfile

docker-compose.yml

requirements.txt

Crear el fichero .gitignore para ignorar:

.venv/

__pycache__/

# 4. Alta del proyecto en Render

Acceder a https://render.com

Iniciar sesión con la cuenta de GitHub

Aceptar los permisos de acceso a los repositorios


# 5 Creación de la base de datos PostgreSQL en Render

En Render, pulsar New → Postgre

Seleccionar la región Frankfurt (EU Central)

Asignar un nombre a la base de datos

Crear el servicio

# 6. Creación del servicio web

Pulsar New → Web Service

Seleccionar el repositorio del proyecto MotosAPI

Acceder a la pantalla de configuración del servicio

Copiar de la base de datos url interna crear variable de entorno con la url.
También port

# 7. Despliegue de la aplicación

Guardar la configuración

Render iniciará automáticamente el proceso de despliegue

Se instalarán las dependencias

Se arrancará la aplicación con Uvicorn

Render proporcionará una URL pública