from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)

    name = Column(String)
    surname = Column(String)
    email = Column(String,unique=True)
    password = Column(String)    
    avatar = Column(String)

    students_issue_fk = relationship('Issue',back_populates='issues_students_fk')
    students_answers_fk = relationship('Answer', back_populates='answers_students_fk')

class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    
    name = Column(String)
    date = Column(String)
    id_student = Column(Integer,ForeignKey('students.id'))

    # 1 párametro es la clase la cual se relacionara,la segunda el nombre de la columna
    issues_students_fk = relationship('Student',back_populates='students_issue_fk')
    issues_answers_fk = relationship('Answer',back_populates='answers_issues_fk')


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)

    content = Column(String)
    date = Column(String)
    id_student = Column(Integer,ForeignKey('students.id'))
    id_issue = Column(Integer,ForeignKey('issues.id'))

    answers_students_fk = relationship('Student',back_populates='students_answers_fk')
    answers_issues_fk = relationship('Student', back_populates='issues_answers_fk')