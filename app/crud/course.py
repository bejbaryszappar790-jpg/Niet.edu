from sqlalchemy.orm import Session
from app.models import Course, Enrollment, Workshop, Teacher

def get_course(db : Session, course_id : int):
    result = db.query(Course).filter(Course.course_id == course_id).first()
    return result


def get_courses_for_student(db : Session, student_id : int):
    courses = db.query(Course).join(Enrollment, Enrollment.course_id == Course.course_id).filter(Enrollment.student_id == student_id).distinct().all()
    return courses

def get_courses_for_teacher(db: Session, teacher_id : int):
    courses = db.query(Course).join(Workshop, Workshop.course_id == Course.course_id).filter(Workshop.teacher_id == teacher_id).distinct().all()
    return courses



def create_course(db : Session, course_name : str, course_sphere : str, teacher_email : str, teacher_password : str):
    teacher = db.query(Teacher).filter(Teacher.teacher_email == teacher_email, Teacher.teacher_password == teacher_password).first()
    
    if teacher != None:
        check_course = db.query(Course).filter(Course.course_name == course_name, Course.course_sphere == course_sphere).first()
        
        if check_course != None:
            check_workshop = db.query(Workshop).filter(Workshop.course_id == check_course.course_id, Workshop.teacher_id == teacher.teacher_id).first()
            
            if check_workshop == None:
                
                new_workshop = Workshop(teacher_id = teacher.teacher_id, course_id = check_course.course_id)
                db.add(new_workshop)
                db.commit()
                return check_course
            else:
                return check_course
        else:
            new_course = Course(course_name = course_name, course_sphere = course_sphere)
            db.add(new_course)
            db.commit()
            db.refresh(new_course)

            new_workshop = Workshop(teacher_id = teacher.teacher_id, course_id = new_course.course_id)
            db.add(new_workshop)
            db.commit()
            return new_course
    
    
