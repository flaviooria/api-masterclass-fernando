from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from db import SQLModel, engine
from routers import issues, students, answers

app = FastAPI(title='Api Fernando Responde')
oauth2 = OAuth2PasswordBearer(tokenUrl='/auth')
PREFIX_VERSION_API = '/api/v1'

# Crearemos el contexto para generar el cifrado de la contraseña
context = CryptContext(schemes=['bcrypt'])

# Add cors, esto nos permite aceptar peticiones de clientes externos o al que demos acceso
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=["*"]
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Add routers, rutas que vamos a establecer para las peticiones
app.include_router(students.router, prefix=PREFIX_VERSION_API)
app.include_router(issues.router, prefix=PREFIX_VERSION_API)
app.include_router(answers.router, prefix=PREFIX_VERSION_API)
