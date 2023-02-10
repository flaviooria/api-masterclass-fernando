from pydantic import BaseModel
from datetime import datetime

class Students(BaseModel):
    uuid: str | None = ''
    name: str | None = ''
    surname: str | None = ''
    avatar: str | None = ''
    email: str | None = ''


class StudentsDB(Students):
    password: str

class StudentRegisterForm(BaseModel):
    name: str
    surname: str
    email: str
    password: str