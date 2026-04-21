from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func


class Student(Base):
    __tablename__ = "Student"
    student_id = Column(Integer, primary_key=True, index = True)
    student_first_name = Column(String, nullable = False)
    student_last_name = Column(String, nullable = False)
    student_email = Column(String, unique = True, index = True, nullable = False)
    student_password = Column(String, nullable = False)


class Teacher(Base):
    __tablename__ = "Teacher"
    teacher_id = Column(Integer, primary_key = True, index = True)
    teacher_first_name = Column(String, nullable = False)
    teacher_last_name = Column(String, nullable = False)
    teacher_email = Column(String, unique = True, nullable = False)
    teacher_password = Column(String, nullable = False)
    

class Course(Base):
    __tablename__ = "Course"
    course_id = Column(Integer, primary_key = True, index = True)
    course_name = Column(String, nullable = False)
    course_sphere = Column(String, nullable = False)

class Enrollment(Base):
    __tablename__ = "Enrollment"
    enrollment_id = Column(Integer, primary_key = True, index = True)
    student_id = Column(Integer, ForeignKey("Student.student_id"),  nullable = False)
    course_id = Column(Integer, ForeignKey("Course.course_id"), nullable = False)
    enrolled_at = Column(DateTime(timezone = True), server_default = func.now())


class Workshop(Base):
    __tablename__ = "Workshop"
    workshop_id = Column(Integer, primary_key = True, index = True)
    course_id = Column(Integer, ForeignKey("Course.course_id"), nullable = False)
    teacher_id = Column(Integer, ForeignKey("Teacher.teacher_id"), nullable = False)
    workshop_date = Column(DateTime(timezone = True), server_default = func.now())

class Video(Base):
    __tablename__ = "Video"
    video_id = Column(Integer, primary_key = True)
    workshop_id = Column(Integer, ForeignKey("Workshop.workshop_id"), nullable = False)
    video_name = Column(String, nullable = False)
    
class Progress(Base):
    __tablename__ = "Progress"
    progress_id = Column(Integer, primary_key = True)
    student_id = Column(Integer, ForeignKey("Student.student_id"), nullable = False)
    video_id = Column(Integer, ForeignKey("Video.video_id"), nullable = False)
    is_watched = Column(Boolean, default = False)
    watched_on = Column(DateTime(timezone = True), server_default = func.now())
    last_position = Column(Integer, default = 0, nullable = False)
    
    