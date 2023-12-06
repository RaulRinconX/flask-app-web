from fastapi import FastAPI, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from jose import jwt, jwk, jws
from jose.utils import base64url_decode
from dotenv import load_dotenv

import os
import httpx


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
async def agregar_historia_clinica(historia: HistoriaClinica):
    await db.historias.insert_one(historia.dict())
    return {"message": "Historia Clínica added"}

# @app.get("/historias-clinicas/{cedula}")
# async def leer_historia_clinica(cedula: str):
#     historia = await db.historias.find_one({"cedula": cedula})
#     if historia:
#         # Convertir ObjectId a string
#         historia['_id'] = str(historia['_id'])
#         return historia
#     raise HTTPException(status_code=404, detail=f"Historia Clínica not found for cedula {cedula}")



async def get_jwks():
    jwks_url = f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/jwks.json'
    resp = httpx.get(jwks_url)
    return resp.json()

async def verify_jwt(token: str):
    jwks = await get_jwks()
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                jwk.construct(rsa_key),
                algorithms=["RS256"],
                audience=os.getenv("AUTH0_AUDIENCE"),
                issuer=f'https://{os.getenv("AUTH0_DOMAIN")}/'
            )
            return payload
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Error verifying JWT token")

    raise HTTPException(status_code=401, detail="Unable to find appropriate key")


# retorna la información del usuario actual
@app.get("/historias-clinicas/me")
async def get_current_user_role(request: Request):
    auth_header = request.headers.get('Cookie')
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = auth_header.split(" ")[1]
    payload = await verify_jwt(token)
    return payload