from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.schemas.teacher import Teacher_Registration, Teacher_Output
from app.schemas.student import  Student_Output
from app.crud.teacher import get_teacher_by_email, create_teacher
from app.crud.student import get_student, get_student_by_email, get_students
from app.database import get_db

router = APIRouter(prefix = "/teachers", tags = ["Teachers"])

@router.post("/create_teacher", response_model = Teacher_Output)
def register_teacher(teacher_in : Teacher_Registration, db : Session = Depends(get_db)):
        check_teacher_email = get_teacher_by_email(db = db, teacher_email = teacher_in.teacher_email)
        if check_teacher_email:
          raise HTTPException(status_code = 400, detail = "Teacher already exists!")
        else:
            result = create_teacher(db = db, teacher_first_name = teacher_in.teacher_first_name, teacher_last_name = teacher_in.teacher_last_name, teacher_email = teacher_in.teacher_email, teacher_password = teacher_in.teacher_password)
            return result
        
    
@router.get("/get_student", response_model = Student_Output)
def show_student_to_teacher(student_id : int, db : Session = Depends(get_db)):
    student = get_student(db = db, student_id = student_id)
    if student:
        return student
    else:
        raise HTTPException(status_code = 404, detail = "There is no such student with this id!")
    

@router.get("/get_student_by_email", response_model = Student_Output)
def show_student_to_teacher_by_email(student_email : EmailStr, db : Session = Depends(get_db)):
    student = get_student_by_email(db = db, student_email = student_email)
    if student:
        return student
    else:
        raise HTTPException(status_code = 404, detail = "There is no such student with this email")

@router.get("/get_students", response_model = list[Student_Output])
def show_students_to_teacher(teacher_id : int, course_id : int, db : Session = Depends(get_db)):
    students = get_students(db = db, teacher_id = teacher_id, course_id = course_id)
    if students:
        return students
    else:
        raise HTTPException(status_code = 404, detail = "The students were not found!")
    
