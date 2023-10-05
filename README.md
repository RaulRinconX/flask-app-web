## Primero, crear un entorno virtual:

python -m virtualenv env

## Activar el entorno virtual:

. venv/bin/activate

## Para instalar los paquetes necesarios:

pip install -r requirements.txt

## Crear un archivo .env (en la raíz del proyecto) para las variables de entorno:

SECRET_KEY=SECRET_KEY

PGSQL_HOST=host

PGSQL_USER=user

PGSQL_PASSWORD=password

PGSQL_DB=database
