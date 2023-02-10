from utils import readJson, writeJson

from entities import StudentEntity

class StudentService():
    FILE_PATH = './db/students.json'

    def getStudents() -> list | dict:
        students = readJson(StudentService.FILE_PATH)
        users_entity = []
        for email in students:
            users_entity.append(dict(StudentEntity(**students[email])))

        return users_entity
        
    def getStudentByEmail(email: str) -> StudentEntity  | None:
        students = StudentService.getStudents()
        
        for student in students:
            if email != student['email']:
                continue

            return student
    
        return None