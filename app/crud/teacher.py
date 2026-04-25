from sqlalchemy.orm import Session
from app.models import Teacher, Enrollment, Workshop

def get_teacher(db : Session, teacher_id : int):
    result = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    return result

def get_teacher_by_email(db : Session, teacher_email : str):
    result = db.query(Teacher).filter(Teacher.teacher_email == teacher_email).first()
    return result


def get_teachers_for_exact_student(db : Session, student_id : int, course_id : int):
    teacher = db.query(Teacher).join(Workshop, Workshop.teacher_id == Teacher.teacher_id).join(Enrollment, Enrollment.course_id == Workshop.course_id).filter(Enrollment.course_id == course_id, Enrollment.student_id == student_id, Workshop.course_id == course_id).distinct().all()
    return teacher

def create_teacher(db : Session, teacher_first_name : str, teacher_last_name : str, teacher_email : str, teacher_password : str):
    new_teacher = Teacher(teacher_first_name = teacher_first_name, teacher_last_name = teacher_last_name, teacher_email = teacher_email, teacher_password = teacher_password)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher
