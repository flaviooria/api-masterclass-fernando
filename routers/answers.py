from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlmodel import Session, select

from db import engine
from models import Answer, AnswerResponse, StudenBase, Student

router = APIRouter(prefix='/answers', tags=['answers'])

def getSession():
    with Session(engine) as session:
        yield session

def convertToStudentBase(student: Student):
    return StudenBase(**dict(student))

@router.get('/{id_issue}',status_code=200)
def getAnswersByIdIssue(*, db: Session = Depends(getSession), id_issue: int = Path(default=...,alias='id_issue',title='Issue\'s id from table issues')) -> list[AnswerResponse]:
    answers = db.exec(select(Answer).where(Answer.issue_id ==  id_issue)).all()

    if not answers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Answers not founded in db')
    
    answers_responses: list[AnswerResponse] = []
    for answer in answers:
        student = db.exec(select(Student).where(Student.id == answer.student_id)).first()
        student_base = convertToStudentBase(student)
        answer_response = AnswerResponse(id = answer.id, content = answer.content, date= answer.date, student= student_base)
        answers_responses.append(answer_response)

    return answers_responses
    

@router.post('/',status_code=201, response_model=Answer)
def createAnswer(*, db: Session = Depends(getSession), answer: Answer):
    answer.date = datetime.now().strftime('%x %X')
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer
