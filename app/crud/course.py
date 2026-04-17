from sqlalchemy.orm import Session
from app.models import Course

def get_course(db : Session, id : int):
    result = db.query(Course).filter(Course.id == id).first()
    return result


def create_course(db : Session, course_name : str, course_sphere : str):
    new_course = Course(course_name = course_name, course_sphere = course_sphere)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

