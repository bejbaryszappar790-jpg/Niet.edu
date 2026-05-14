from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.teacher import Teacher_Registration, Teacher_Output
from app.schemas.student import Student_Output
from app.schemas.courses import Course_Registration, Output_Schema
from app.schemas.video import Video_Upload, Video_Output
from app.schemas.token import Token_Base
from app.crud.teacher import get_teacher_by_email, create_teacher, login_existing_teacher
from app.crud.student import get_student, get_student_by_email, get_students
from app.crud.course import create_course, get_courses_for_teacher
from app.crud.video import upload_video, get_video_for_teacher
from app.core.security import create_access_token, get_current_teacher
from app.database import get_db

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.post("/create_teacher", response_model=Teacher_Output)
def register_teacher(teacher_in: Teacher_Registration, db: Session = Depends(get_db)):
    check_teacher_email = get_teacher_by_email(
        db=db, teacher_email=teacher_in.teacher_email
    )
    if check_teacher_email:
        raise HTTPException(status_code=400, detail="Teacher already exists!")
    else:
        result = create_teacher(
            db=db,
            teacher_first_name=teacher_in.teacher_first_name,
            teacher_last_name=teacher_in.teacher_last_name,
            teacher_email=teacher_in.teacher_email,
            teacher_password=teacher_in.teacher_password,
        )
        return result



@router.post("/teacher_login", response_model = Token_Base)
def teacher_sign_in(teacher_email : str, teacher_plain_password : str, db : Session = Depends(get_db)):
    check_teacher = get_teacher_by_email(db = db, teacher_email = teacher_email)
    
    if check_teacher:
        result_of_login = login_existing_teacher(db = db, teacher_email = teacher_email, teacher_plain_password = teacher_plain_password)
        
        if result_of_login:
            data = {"sub" : str(result_of_login.teacher_id)}
            access_token = create_access_token(data)

            result = {"access_token" : access_token, "token_type" : "bearer"}
            return result 
        raise HTTPException(status_code = 400, detail = "Email or password is invalid")
    raise HTTPException(status_code = 404, detail = "Teacher was not found")
        
    

@router.get("/get_student", response_model=Student_Output)
def show_student_to_teacher(student_id: int, db: Session = Depends(get_db)):
    student = get_student(db=db, student_id=student_id)
    if student:
        return student
    else:
        raise HTTPException(
            status_code=404, detail="There is no such student with this id!"
        )


@router.get("/get_student_by_email", response_model=Student_Output)
def show_student_to_teacher_by_email(
    student_email: EmailStr, db: Session = Depends(get_db)
):
    student = get_student_by_email(db=db, student_email=student_email)
    if student:
        return student
    else:
        raise HTTPException(
            status_code=404, detail="There is no such student with this email"
        )


@router.get("/get_students", response_model=list[Student_Output])
def show_students_to_teacher(
    course_id: int, current_teacher: int = Depends(get_current_teacher),  db: Session = Depends(get_db)
):
    students = get_students(db=db, teacher_id=current_teacher.teacher_id, course_id=course_id)
    if students:
        return students
    else:
        raise HTTPException(status_code=404, detail="The students were not found!")


@router.post("/new_course", response_model=Output_Schema)
def create_course_for_teacher(
    registration_data: Course_Registration, db: Session = Depends(get_db)
):

    new_course = create_course(
        db=db,
        course_name=registration_data.course_name,
        course_sphere=registration_data.course_sphere,
        teacher_email=registration_data.teacher_email,
        teacher_hashed_password=registration_data.teacher_hashed_password,
    )
    if new_course:
        return new_course
    else:
        raise HTTPException(status_code=401, detail="The teacher was not found!")


@router.get("/teacher_courses", response_model=list[Output_Schema])
def show_courses_to_teacher(current_teacher: int = Depends(get_current_teacher), db: Session = Depends(get_db)):
    courses = get_courses_for_teacher(db=db, teacher_id=current_teacher.teacher_id)
    if courses:
        return courses
    else:
        raise HTTPException(status_code=404, detail="Courses were not found!")


@router.post("/teacher_video", response_model=Video_Output)
def create_video_for_teacher(video_in: Video_Upload, current_teacher: int = Depends(get_current_teacher), db: Session = Depends(get_db)):
    check_video = get_video_for_teacher(
        db=db,
        course_id=video_in.course_id,
        teacher_id=current_teacher.teacher_id,
        video_url=video_in.video_url,
    )
    if check_video:
        return check_video
    else:
        try:
            new_video = upload_video(
                db=db,
                course_id=video_in.course_id,
                teacher_id=current_teacher.teacher_id,
                video_name=video_in.video_name,
                video_url=video_in.video_url,
                video_description=video_in.video_description,
                video_order_id=video_in.video_order_id,
            )
            
            if not new_video:
                raise HTTPException(status_code = 400, detail = "URL is not valid")
            
            return new_video
        except IntegrityError:
            raise HTTPException(status_code=400, detail="The order id is not available")
