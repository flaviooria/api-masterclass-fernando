from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlmodel import Session, select

from datetime import datetime

from db import engine
from models import Issue, IssueBase

router = APIRouter(prefix='/issues', tags=['issues'])


def convertToIssueBase(issue: Issue) -> dict:
    return dict(IssueBase(**dict(issue)))

def getSession():
    with Session(engine) as session:
        yield session


@router.get('/',status_code=200,response_model=list[IssueBase])
def getIssues(*, db: Session = Depends(getSession)):
    issues =  db.exec(select(Issue)).all()
    return list(map(convertToIssueBase,issues))

@router.get('/{id_issue}', status_code=200, response_model=Issue)
def getIssueById(*, db: Session = Depends(getSession), id: int = Path(default=...,alias='id_issue',title='Issue\'s id in database')):
    founded_issue = db.exec(select(Issue).where(Issue.id == id)).first()

    if not founded_issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Issue not found')
    
    return founded_issue

@router.post('/', status_code=201, response_model=IssueBase)
def createIssue(*,db: Session = Depends(getSession), issue: Issue):
    issue.date = datetime.now().strftime('%x %X')
    db.add(issue)
    db.commit()
    # Solo aplicar el refresh si hemos hecho cambios directamente en el issue
    db.refresh(issue)

    return issue