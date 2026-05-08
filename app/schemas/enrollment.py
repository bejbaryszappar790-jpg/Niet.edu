from pydantic import BaseModel


class Enrollment_Base(BaseModel):
    course_id : int
    teacher_id : int


class Enrollment_Input(Enrollment_Base):
    student_id : int
    

class Enrollment_Output(Enrollment_Base):
    teacher_first_name : str
    teacher_last_name : str
    course_name : str
    course_sphere : str
    class Config:
        from_attributes = True