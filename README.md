## Primero, crear un entorno virtual:

python -m virtualenv env

## Activar el entorno virtual:

. venv\Scripts\activate

## Para instalar los paquetes necesarios:

pip install -r requirements.txt

## Crear un archivo .env (en la raíz del proyecto) para las variables de entorno:

SECRET_KEY=SECRET_KEY

PGSQL_HOST=10.128.0.10

PGSQL_USER=monitoring_user

PGSQL_PASSWORD=rasi

PGSQL_DATABASE=monitoring_db
