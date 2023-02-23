from sqlmodel import Field, SQLModel, Relationship
from enum import Enum
from pydantic import BaseModel

class AsignatureEnum(str,Enum):
    DAW = 'DAW'
    DAM_= 'DAM'

class Token(SQLModel):
    access_token: str
    token_type: str


class Asignature(SQLModel, table=True):
    id: int = Field(default=None,primary_key=True)
    name: AsignatureEnum

class StudentUpdate(SQLModel):
    name: str | None
    surname: str | None
    email: str | None
    avatar: str | None


class StudenBase(SQLModel):
    name: str
    surname: str
    email: str
    avatar: str | None

class StudentResponse(StudenBase):
    id: int

class StudentMe(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    avatar: str

class StudentAuth(SQLModel):
    email: str
    password: str


class Student(StudenBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str
    token: str | None
    
    # Vamos a usar la clase relation, ya que tendremos una relación entre nuesta clase student y issue
    # en back_populates = nombre de la variable del modelo issue que refiere al modelo student
    issues: list["Issue"] = Relationship(back_populates='student')
    answers_student: list["Answer"] = Relationship(back_populates='students')

class IssueBase(SQLModel):
    id: int
    name: str
    date: str | None
    category: str
    asignature: AsignatureEnum

class Issue(IssueBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Crearemos nuesta clave foranea, este se relaciona con la tabla student
    student_id: int = Field(default=None,foreign_key='student.id')

    student: Student | None = Relationship(back_populates='issues')
    answers_issues: list["Answer"] = Relationship(back_populates='answers')

class Answer(SQLModel, table= True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    date: str | None

    student_id: int = Field(default=None, foreign_key='student.id')
    issue_id: int = Field(default=None, foreign_key='issue.id')

    students: Student | None = Relationship(back_populates='answers_student')
    answers: Issue | None = Relationship(back_populates='answers_issues')


class AnswerResponse(SQLModel):
    id: int | None
    content: str
    date: str | None
    student: StudenBase
