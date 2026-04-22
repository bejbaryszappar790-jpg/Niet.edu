from pydantic import BaseModel, EmailStr

class Course_Base(BaseModel):
    course_name : str
    course_sphere : str
    
class Course_Registration(Course_Base):
    teacher_email : EmailStr
    teacher_password : str

class Output_Schema(Course_Base):
    course_id : int
    class Config:
        from_attributes = True

    