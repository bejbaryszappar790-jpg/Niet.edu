from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.schemas.student import Student_Registration, Student_Output
from app.schemas.teacher import Teacher_Output
from app.crud.student import create_student, get_student_by_email
from app.crud.teacher import get_teachers_for_exact_student, get_teacher, get_teacher_by_email
from app.crud.course import get_courses_for_student
from app.database import get_db

router = APIRouter(prefix = "/students", tags = ["Students"])


@router.post("/new_student", response_model = Student_Output)
def register_student(student_in : Student_Registration, db : Session = Depends(get_db)):
    check_student = get_student_by_email(db = db, student_email = student_in.student_email)
    
    if check_student:
        raise HTTPException(status_code = 400, detail = "The student already exists!")
    else:
        student = create_student(db = db, student_first_name = student_in.student_first_name, student_last_name = student_in.student_last_name, student_email = student_in.student_email, student_password = student_in.student_password)
        return student
    

@router.get("/my_teacher", response_model = Teacher_Output)
def show_teacher_to_student(teacher_id : int, db : Session = Depends(get_db)):
    teacher =  get_teacher(db = db, teacher_id = teacher_id)
    if teacher:
        return teacher
    else:
        raise HTTPException(status_code = 404, detail = "The teacher was not found!")


@router.get("/teacher_email", response_model = Teacher_Output)
def show_teacher_to_student_by_email(teacher_email : EmailStr, db : Session = Depends(get_db)):
    teacher = get_teacher_by_email(db = db, teacher_email = teacher_email)
    if teacher:
        return teacher
    else:
        raise HTTPException(status_code = 404, detail = "The teacher was not found!")
    

@router.get("/my_teachers", response_model = list[Teacher_Output])
def show_teachers_to_student(student_id : int, course_id : int, db : Session = Depends(get_db)):
    teachers = get_teachers_for_exact_student(db = db, student_id = student_id, course_id = course_id)
    if teachers:
        return teachers
    else:
        raise HTTPException(status_code = 404, detail = "Teachers were not found!")
    

@router.get("/my_courses")
def show_courses_to_student(student_id : int, db : Session = Depends(get_db)):
    courses = get_courses_for_student(db = db, student_id = student_id)
    if courses:
        return courses
    else:
        raise HTTPException(status_code = 404, detail = "Courses were not found!")



