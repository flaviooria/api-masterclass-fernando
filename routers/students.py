from fastapi import APIRouter, Query

from services import StudentService

router = APIRouter(prefix='/students',tags=['students'])

@router.get('/',status_code=200)
def getStudents():
    return []
