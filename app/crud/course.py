from sqlalchemy.orm import Session
from app.models import Course, Enrollment, Workshop, Teacher, Student



def get_course(db: Session, course_id: int):
    result = db.query(Course).filter(Course.course_id == course_id).first()
    return result


def get_courses_for_student(db: Session, student_id: int):
    courses = (
        db.query(
            Course.course_id, 
            Course.course_name, 
            Course.course_sphere,
            Teacher.teacher_first_name,
            Teacher.teacher_last_name, 
            Teacher.teacher_id
            )
        .select_from(Enrollment)
        .join(Course, Enrollment.course_id == Course.course_id)
        .join(Teacher, Enrollment.teacher_id == Teacher.teacher_id)
        .filter(Enrollment.student_id == student_id)
        .distinct()
        .all()
    )
    return courses


def get_courses_for_teacher(db: Session, teacher_id: int):
    courses = (
        db.query(Course)
        .join(Workshop, Workshop.course_id == Course.course_id)
        .filter(Workshop.teacher_id == teacher_id)
        .distinct()
        .all()
    )
    return courses


def get_enrollment_details(db: Session, student_id : int, course_id : int, teacher_id : int):
    return db.query(
                Enrollment.course_id, 
                Enrollment.teacher_id,
                Enrollment.student_id,
                Course.course_name,
                Course.course_sphere,
                Teacher.teacher_first_name,
                Teacher.teacher_last_name
            ).join(Course, Enrollment.course_id == Course.course_id)\
             .join(Teacher, Enrollment.teacher_id == Teacher.teacher_id)\
             .filter(
                 Enrollment.student_id == student_id, 
                 Enrollment.course_id == course_id, 
                 Enrollment.teacher_id == teacher_id
                 )\
             .first()

def new_course_for_student(db: Session, student_id : int, course_id : int, teacher_id : int):
    check_student = db.query(Student).filter(Student.student_id == student_id).first()
    check_course = db.query(Course).filter(Course.course_id == course_id).first()
    check_teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()

    if check_student and check_course and check_teacher:
        check_enrollment = db.query(Enrollment)\
            .filter(
                Enrollment.student_id  == student_id, 
                Enrollment.teacher_id == teacher_id, 
                Enrollment.course_id == course_id)\
            .first()
        if check_enrollment:
            
            checked_enrollment_for_user = get_enrollment_details(db = db, student_id = student_id, course_id = course_id, teacher_id = teacher_id)
            return checked_enrollment_for_user
    
        new_enrollment = Enrollment(student_id = student_id, course_id = course_id, teacher_id = teacher_id)
        db.add(new_enrollment)
        db.commit()
        db.refresh(new_enrollment)

        enrollment_for_user = get_enrollment_details(db = db, student_id = student_id, course_id = course_id, teacher_id = teacher_id)

        return enrollment_for_user


def create_course(
    db: Session,
    course_name: str,
    course_sphere: str,
    teacher_id : int
):
   
    existing_course = db.query(Course).filter(Course.course_name == course_name).first()
    
    if existing_course:
        existing_workshop = db.query(Workshop).filter(Workshop.course_id == existing_course.course_id, Workshop.teacher_id == teacher_id).first()

        if not existing_workshop:
            new_workshop = Workshop(course_id = existing_course.course_id, teacher_id = teacher_id)
            db.add(new_workshop)
            db.commit()
        
            return existing_course

        return existing_course
    
    new_course = Course(course_name = course_name, course_sphere = course_sphere)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    new_workshop = Workshop(course_id = new_course.course_id, teacher_id = teacher_id)
    db.add(new_workshop)
    db.commit()


    return new_course
    
