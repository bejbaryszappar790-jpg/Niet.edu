from sqlalchemy.orm import Session
from app.models import Teacher

def get_teacher(db : Session, teacher_id : int):
    result = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    return result

def get_teacher_by_email(db : Session, email : str):
    result = db.query(Teacher).filter(Teacher.email == email).first()
    return result

def create_teacher(db : Session, teacher_first_name : str, teacher_last_name : str, teacher_email : str, teacher_password : str):
    new_teacher = Teacher(teacher_first_name = teacher_first_name, teacher_last_name = teacher_last_name, teacher_email = teacher_email, teacher_password = teacher_password)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher
