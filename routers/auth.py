import uuid

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from entities import StudentDbEnity, StudentEntity, StudentRegisterForm
from routers import students
from utils import readJson, writeJson, generateUUID

router = APIRouter(prefix='/auth',tags=['auth'])
oauth2 = OAuth2PasswordBearer(tokenUrl='/jwt')
PREFIX_VERSION_API = '/api/v1'
# Crearemos el contexto para generar el cifrado de la contraseña
context = CryptContext(schemes=['bcrypt'])


def isValidEmailWithDomain(email: str) -> bool:
    posTo = email.find('@')
    print(posTo)
    domain = email[posTo + 1:]
    print(domain)
    return domain in 'fernando.es'


def getAvatar(name : str, surname: str) -> str:
    name = name.strip()
    surname = surname.strip()
    return f'https://ui-avatars.com/api/?name={name}+{surname}&background=random'


def getStudentBD(email: str) -> StudentDbEnity | None:
    users = readJson('./db/students.json')
    if email in users:
        founded_user = dict(users[email])
        return StudentDbEnity(**founded_user)
    

@router.post('/signUp',status_code=201, response_model=StudentEntity)
async def register(student: StudentRegisterForm):
    students_in_db = readJson('./db/students.json')

    if not student.name or not student.email or not student.password or not student.surname:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='parameters not found in fields')
    
    # Verificamos que el email tenga como dominio fernando.es
    if not isValidEmailWithDomain(student.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email not correspond with domain')
    
    # Verificamos si el correo ya existe en la base de datos 
    if student.email in students_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')

    student_db = StudentDbEnity(**dict(student))
    student_db.uuid = generateUUID()
    avatar = getAvatar(student_db.name, student_db.surname)
    student_db.avatar = avatar
    student_db.password = context.hash(student_db.password)
    db = {student_db.email: dict(student_db)}

    writeJson('./db/students.json',data=db)

    return db


@router.post('/signIn',status_code=200, response_model=StudentEntity)
async def login(student: OAuth2PasswordRequestForm = Depends()):
    users = readJson('./db/students.json')

    if not student.username in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Student not found')
    
    founded_user = getStudentBD(student.username)

    if not context.verify(student.password, founded_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password incorrect')
    
    return dict(founded_user)