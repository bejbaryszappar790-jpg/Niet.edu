from sqlalchemy.orm import Session
from app.models import Teacher

def get_teacher(db : Session, id : int):
    result = db.query(Teacher).filter(Teacher.id == id).first()
    return result

def get_teacher_by_email(db : Session, email : str):
    result = db.query(Teacher).filter(Teacher.email == email).first()
    return result

def create_teacher(db : Session, first_name : str, last_name : str, email : str, password : str):
    new_teacher = Teacher(first_name = first_name, last_name = last_name, email = email, password = password)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher
