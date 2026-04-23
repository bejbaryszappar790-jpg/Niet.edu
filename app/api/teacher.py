from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.teacher import Teacher_Registration, Teacher_Output
from app.crud.teacher import get_teacher, get_teacher_for_exact_student, get_teacher_by_email, create_teacher
from app.database import get_db

router = APIRouter(prefix = "/teachers", tags = ["Teachers"])

@router.post("/create_teacher", response_model = Teacher_Output)
def register_teacher(teacher_in : Teacher_Registration, db : Session = Depends(get_db)):
        check_teacher_email = get_teacher_by_email(db = db, teacher_email = teacher_in.teacher_email)
        if check_teacher_email != None:
          raise HTTPException(status_code = 400, detail = "Teacher already exists!")
        else:
            result = create_teacher(db = db, teacher_first_name = teacher_in.teacher_first_name, teacher_last_name = teacher_in.teacher_last_name, teacher_email = teacher_in.teacher_email, teacher_password = teacher_in.teacher_password)
            return result