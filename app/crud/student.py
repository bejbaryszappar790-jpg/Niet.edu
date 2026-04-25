from sqlalchemy.orm import Session
from app.models import Student, Workshop, Enrollment


def get_student(db : Session, student_id : int):

    result = db.query(Student).filter(Student.student_id == student_id).first()
    return result


def get_student_by_email(db: Session, student_email : str):
    result = db.query(Student).filter(Student.student_email == student_email).first()
    return result


def get_students(db : Session, teacher_id : int, course_id : int):
    students = db.query(Student).join(Enrollment, Enrollment.student_id == Student.student_id).join(Workshop, Enrollment.course_id == Workshop.course_id).filter(Workshop.teacher_id == teacher_id, Workshop.course_id == course_id).distinct().all()
    return students


    
def create_student(db : Session, student_first_name : str, student_last_name : str, student_email : str, student_password : str):
    new_student = Student(student_first_name = student_first_name, student_last_name = student_last_name, student_email = student_email, student_password = student_password)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


