from pydantic import BaseModel, EmailStr

class Teacher_Base(BaseModel):
    teacher_first_name: str
    teacher_last_name: str
    
class Teacher_Registration(Teacher_Base):
    teacher_email: EmailStr
    teacher_password: str

class Teacher_Output(Teacher_Base):
    teacher_id: int
    class Config:
        from_attributes = True