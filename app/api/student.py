from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.schemas.student import Student_Registration, Student_Output
from app.schemas.teacher import Teacher_Output
from app.schemas.courses import Output_Schema
from app.schemas.video import Video_Output
from app.schemas.enrollment import Enrollment_Input, Enrollment_Output
from app.schemas.progress import Progress_Input, Progress_Output
from app.crud.student import create_student, get_student_by_email
from app.crud.teacher import (
    get_teachers_for_exact_student,
    get_teacher,
    get_teacher_by_email,
)
from app.crud.course import get_courses_for_student, new_course_for_student
from app.crud.video import get_all_videos_from_course
from app.crud.progress import upload_progress
from app.database import get_db

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/new_student", response_model=Student_Output)
def register_student(student_in: Student_Registration, db: Session = Depends(get_db)):
    check_student = get_student_by_email(db=db, student_email=student_in.student_email)

    if check_student:
        raise HTTPException(status_code=400, detail="The student already exists!")
    else:
        student = create_student(
            db=db,
            student_first_name=student_in.student_first_name,
            student_last_name=student_in.student_last_name,
            student_email=student_in.student_email,
            student_password=student_in.student_password,
        )
        return student


@router.post("/course_enrollment", response_model = Enrollment_Output)
def enroll_to_course(enroll_in : Enrollment_Input, db : Session = Depends(get_db)):
    new_enrollment = new_course_for_student(db = db, student_id = enroll_in.student_id, teacher_id = enroll_in.teacher_id, course_id = enroll_in.course_id)

    if not new_enrollment:
        raise HTTPException(status_code = 400, detail = "Data were invalid!!!")
    
    return new_enrollment


@router.get("/my_teacher", response_model=Teacher_Output)
def show_teacher_to_student(teacher_id: int, db: Session = Depends(get_db)):
    teacher = get_teacher(db=db, teacher_id=teacher_id)
    if teacher:
        return teacher
    else:
        raise HTTPException(status_code=404, detail="The teacher was not found!")


@router.get("/teacher_email", response_model=Teacher_Output)
def show_teacher_to_student_by_email(
    teacher_email: EmailStr, db: Session = Depends(get_db)
):
    teacher = get_teacher_by_email(db=db, teacher_email=teacher_email)
    if teacher:
        return teacher
    else:
        raise HTTPException(status_code=404, detail="The teacher was not found!")


@router.get("/my_teachers", response_model=list[Teacher_Output])
def show_teachers_to_student(
    student_id: int, course_id: int, db: Session = Depends(get_db)
):
    teachers = get_teachers_for_exact_student(
        db=db, student_id=student_id, course_id=course_id
    )
    if teachers:
        return teachers
    else:
        raise HTTPException(status_code=404, detail="Teachers were not found!")


@router.get("/my_courses", response_model=list[Output_Schema])
def show_courses_to_student(student_id: int, db: Session = Depends(get_db)):
    courses = get_courses_for_student(db=db, student_id=student_id)
    if courses:
        return courses
    else:
        raise HTTPException(status_code=404, detail="Courses were not found!")


@router.get("/my_videos", response_model=list[Video_Output])
def show_videos_to_student(
    student_id: int, course_id: int, teacher_id: int, db: Session = Depends(get_db)
):
    videos = get_all_videos_from_course(
        db=db, student_id=student_id, course_id=course_id, teacher_id=teacher_id
    )

    if videos:
        return videos
    else:
        raise HTTPException(status_code=404, detail="Videos were not found!")
    
@router.post("/into_video", response_model = Progress_Output)
def work_with_progress(progress_in : Progress_Input, db : Session = Depends(get_db)):
    result = upload_progress(db = db, student_id = progress_in.student_id, video_id = progress_in.video_id, last_position = progress_in.last_position)
    
    if result:
        return result
    
    raise HTTPException(status_code = 404, detail = "The video was not found!!!")