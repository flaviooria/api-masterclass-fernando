from datetime import datetime, timedelta
import os

from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from db import engine
from models import (Issue, IssueBase, StudenBase, Student, StudentAuth,
                    StudentResponse, Token, StudentUpdate)

#oauth2 para validar las peticiones que nos haga despúes el cliente 
oauth2 = OAuth2PasswordBearer(tokenUrl='/auth')
# Contenxto que servira para crear el hash de las contraseñas de los estudiantes
context = CryptContext(schemes=['bcrypt'])
router = APIRouter(prefix='/students', tags=['students'])

# Añadiremos un secrete para proporcionarle más seguridad al jwt => openssl rand -hex 32 en linux 
SECRET = os.getenv('SECRET')
# Tiempo de expiración para el token
TIME_EXPIRES_TOKEN = 30
# Añadimos el algoritmo que usa jwt
ALGORITHM = 'HS256'

# Dependencies
def getSession():
    with Session(engine) as session:
        yield session

def currentStudent(token: str = Depends(oauth2), db: Session = Depends(getSession)):
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not found token')
    
    try:
        email_student = jwt.decode(token,SECRET,ALGORITHM)['sub']

        founded_student = db.exec(select(Student).where(Student.email == email_student)).first()

        if not founded_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Student not found')
        
        return StudentResponse(**dict(founded_student))
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    ...

def convertToStudentBase(student: Student) -> dict:
    return dict(StudenBase(**dict(student)))

def convertToStudentResponse(student: Student) -> dict:
    return dict(StudentResponse(**dict(student)))

def convertToIssueBase(issue: Issue) -> dict:
    return dict(IssueBase(**dict(issue)))

def getAvatar(name: str, surname: str) -> str:
    return f'https://ui-avatars.com/api/?background=BACFA9&name={name}+{surname}&rounded=true'


@router.get('/', status_code=200, response_model=list[StudentResponse])
def getStudents(db: Session = Depends(getSession)):
    students_db = db.exec(select(Student)).all()
    return list(map(convertToStudentResponse, students_db))

@router.get('/{id_user}/issues/', status_code=200, response_model=list[IssueBase]) # http://localhost:3000/api/v1/students/2/issues/
def getIssuesByStudentId(*, db: Session = Depends(getSession), id_user: int = Path(default=..., alias='id_user', title='Student\'s id')):

    student = db.exec(select(Student).where(Student.id == id_user)).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Student not found')

    issues = db.exec(select(Issue).where(Issue.student_id == id_user)).all()

    return list(map(convertToIssueBase,issues))

# Auth
@router.post('/me')
def getMe(student: StudentResponse = Depends(currentStudent)):
    return student


@router.post('/signIn',status_code=200, response_model=Token)
def login(*, db: Session = Depends(getSession),form: StudentAuth):
    # Vamos a buscar si el estudiante existe en la base de datos
    email = form.email
    user_in_db = db.exec(select(Student).where(Student.email == email)).first()

    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Student not founded')
    
    # Existe usuario
    # Paso 1 Comprobamos que las contraseñas coincidan
    if not context.verify(form.password, user_in_db.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Password incorrect')
    # Paso 2 Generamos un token
    expiration = datetime.utcnow() + timedelta(minutes=TIME_EXPIRES_TOKEN)
    print(expiration)

    access_token = { 'sub': form.email, 'exp': expiration }
    token = jwt.encode(access_token,SECRET,ALGORITHM)

    return dict(Token(access_token=token,token_type='JWT'))
    

@router.post('/signUp', status_code=201, response_model=StudenBase)
def createStudent(*, db: Session = Depends(getSession), student: Student):
    founded_student = db.exec(select(Student).where(Student.email == student.email)).first()

    if founded_student:
        raise HTTPException(400,detail='Student already exists')

    hash_password = context.hash(student.password)
    student.password = hash_password

    student.avatar = getAvatar(student.name, student.surname)

    db.add(student)
    db.commit()
    db.refresh(student)

    return JSONResponse(content={'status': 201, 'payload': convertToStudentResponse(student)},status_code=201)


@router.patch('/{id_student}')
def updateStudent(*, db: Session = Depends(getSession), id_student: int, student: StudentUpdate):
    founded_student = db.exec(select(Student).where(Student.id == id_student)).first()

    if not founded_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Student not found')
    
    if student.password:
        student.password = context.hash(student.password)

    name = student.name if student.name != None else founded_student.name
    surname = student.surname if student.surname != None else founded_student.surname

    student.avatar = getAvatar(name,surname)
    
    # exclude_unset => sólo incluiría los valores enviados por el cliente.
    student_data = student.dict(exclude_unset=True)

    # setattr => Si no estás familiarizado con setattr(), toma un objeto, como el founded_student, luego un nombre de atributo (clave), que en nuestro caso podría ser "nombre", y un valor (valor). Y luego establece el atributo con ese nombre al valor.

    for key, value in student_data.items():
        setattr(founded_student, key, value)
        
    db.add(founded_student)
    db.commit()
    db.refresh(founded_student)

    return StudentResponse(**dict(founded_student))



