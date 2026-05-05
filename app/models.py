from app.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.sql import func


class Student(Base):
    __tablename__ = "Student"
    student_id = Column(Integer, primary_key=True, index=True)
    student_first_name = Column(String, nullable=False)
    student_last_name = Column(String, nullable=False)
    student_email = Column(String, unique=True, index=True, nullable=False)
    student_password = Column(String, nullable=False)


class Teacher(Base):
    __tablename__ = "Teacher"
    teacher_id = Column(Integer, primary_key=True, index=True)
    teacher_first_name = Column(String, nullable=False)
    teacher_last_name = Column(String, nullable=False)
    teacher_email = Column(String, unique=True, nullable=False)
    teacher_password = Column(String, nullable=False)


class Course(Base):
    __tablename__ = "Course"
    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    course_sphere = Column(String, nullable=False)


class Enrollment(Base):
    __tablename__ = "Enrollment"
    enrollment_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(
        Integer, ForeignKey("Student.student_id"), nullable=False, index=True
    )
    course_id = Column(
        Integer, ForeignKey("Course.course_id"), nullable=False, index=True
    )
    teacher_id = Column(
        Integer, ForeignKey("Teacher.teacher_id"), nullable=False, index=True
    )
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())


class Workshop(Base):
    __tablename__ = "Workshop"
    workshop_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(
        Integer, ForeignKey("Course.course_id"), nullable=False, index=True
    )
    teacher_id = Column(
        Integer, ForeignKey("Teacher.teacher_id"), nullable=False, index=True
    )
    workshop_date = Column(DateTime(timezone=True), server_default=func.now())


class Video(Base):
    __tablename__ = "Video"
    video_id = Column(Integer, primary_key=True)
    course_id = Column(
        Integer, ForeignKey("Course.course_id"), nullable=False, index=True
    )
    teacher_id = Column(
        Integer, ForeignKey("Teacher.teacher_id"), nullable=False, index=True
    )
    video_order_id = Column(Integer, nullable=False, index=True)
    video_name = Column(String, nullable=False)
    video_description = Column(String)
    video_url = Column(String, nullable=False)
    video_duration = Column(Integer, nullable=False)
    video_preview_url = Column(String, nullable=False)
    youtube_id = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "course_id", "teacher_id", "video_order_id", name="video_course_teacher_uc"
        ),
    )


class Progress(Base):
    __tablename__ = "Progress"
    progress_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(
        Integer, ForeignKey("Student.student_id"), nullable=False, index=True
    )
    video_id = Column(Integer, ForeignKey("Video.video_id"), nullable=False, index=True)
    is_watched = Column(Boolean, default=False)
    watched_on = Column(DateTime(timezone=True), server_default=func.now())
    last_position = Column(Integer, default=0, nullable=False)
