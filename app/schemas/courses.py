from pydantic import BaseModel

class Course_Base(BaseModel):
    course_name : str
    course_sphere : str
    
class Create_Course(Course_Base):
    teacher_email : str
    teacher_password : str

class Output_Schema(Course_Base):
    course_id : int
    class Config:
        from_attributes = True

    