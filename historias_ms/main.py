from fastapi import FastAPI, HTTPException, Request, Cookie
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

class HistoriaClinica(BaseModel):
    nombre: str
    cedula: str
    fecha_nacimiento: str
    tipo_sangre: str
    fecha_examen: str
    enfermedades: str
    medicamentos: str
    alergia: str



@app.post("/historias-clinicas/")
async def agregar_historia_clinica(historia: HistoriaClinica, session_id: str = Cookie(None)):
    if session_id and es_sesion_valida(session_id):
        await db.historias.insert_one(historia.dict())
        return {"message": "Historia Clínica added"}
    return {"message": "Acceso denegado", "status": 401}

@app.get("/historias-clinicas/{cedula}")
async def leer_historia_clinica(cedula: str,  session_id: str = Cookie(None)):
    if session_id and es_sesion_valida(session_id):
        historia = await db.historias.find_one({"cedula": cedula})
        if historia:
            # Convertir ObjectId a string
            historia['_id'] = str(historia['_id'])
            return historia
        raise HTTPException(status_code=404, detail=f"Historia Clínica not found for cedula {cedula}")
    return {"message": "Acceso denegado", "status": 401}


def es_sesion_valida(session_id: str):
    print(session_id)
    return True