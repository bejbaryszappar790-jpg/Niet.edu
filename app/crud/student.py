from sqlalchemy.orm import Session
from app.models import Student


def get_student(db : Session, id):

    result = db.query(Student).filter(Student.id == id).first()
    return result

def create_student(db : Session, first_name : str, last_name : str, email : str, password : str):
    new_student = Student(first_name = first_name, last_name = last_name, email = email, password = password)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


