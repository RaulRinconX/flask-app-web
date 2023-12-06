from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from dotenv import load_dotenv


import os


app = FastAPI()

load_dotenv()
# MongoDB connection details
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME")

print(MONGODB_URL)
print(DB_NAME)
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]



IPs_PERMITIDAS = ["34.31.133.98"]  # Añade aquí la IP del microservicio de usuarios

@app.middleware("http")
async def verificar_ip(request: Request, call_next):
    ip_cliente = request.client.host
    if ip_cliente not in IPs_PERMITIDAS:
        # Devolver una respuesta HTML que indique que el acceso no está permitido
        contenido_html = """
            <html>
                <head><title>Acceso Denegado</title></head>
                <body>
                    <h1>Acceso Denegado</h1>
                    <p>No tienes permiso para acceder a esta página.</p>
                    <p><a href="/usuarios">Volver a la página de inicio</a></p>
                </body>
            </html>
        """
        return HTMLResponse(content=contenido_html, status_code=403)

    return await call_next(request)

class HistoriaClinica(BaseModel):
    nombre: str
    cedula: str
    fecha_nacimiento: str
    tipo_sangre: str
    fecha_examen: str
    enfermedades: str
    medicamentos: str
    alergia: str


@app.post("/historias-clinicas-api/")
async def agregar_historia_clinica(historia: HistoriaClinica):
    await db.historias.insert_one(historia.dict())
    return {"message": "Historia Clínica added"}

@app.get("/historias-clinicas-api/")
async def obtener_historias_clinicas():
    historias = await db.historias.find().to_list(1000)
    return historias

