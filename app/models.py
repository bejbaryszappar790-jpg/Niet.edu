from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index = True)
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    email = Column(String, unique = True, index = True, nullable = False)
    password = Column(String, nullable = False)


class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key = True, index = True)
    first_name = Column(String, nullable = False)
    last_name = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key = True, index = True)
    course_name = Column(String, nullable = False)
    course_sphere = Column(String, nullable = False)

class Enrollment(Base):
    __tablename__ = "enrollment"
    id = Column(Integer, primary_key = True, index = True)
    student_id = Column(Integer, ForeignKey("student.id"),  nullable = False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable = False)
    enrolled_at = Column(DateTime(timezone = True), server_default = func.now())


class workshop(Base):
    __tablename__ = "workshop"
    id = Column(Integer, primary_key = True, index = True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable = False)
    teacher_id = Column(Integer, ForeignKey("teacher.id"), nullable = False)
    workshop_date = Column(DateTime(timezone = True), server_default = func.now())

class video(Base):
    __tablename__ = "video"
    id = Column(Integer, primary_key = True)
    workshop_id = Column(Integer, ForeignKey("workshop.id"), nullable = False)
    video_name = Column(String, nullable = False)
    
class progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key = True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable = False)
    video_id = Column(Integer, ForeignKey("video.id"), nullable = False)
    is_watched = Column(Boolean, default = False)
    watched_on = Column(DateTime(timezone = True), server_default = func.now())
    last_position = Column(Integer, default = 0, nullable = False)
    
    