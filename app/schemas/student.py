from pydantic import BaseModel, EmailStr

class Student_Base(BaseModel):
    student_first_name: str
    student_last_name: str

class Student_Registration(Student_Base):
    student_email: EmailStr
    student_password: str

class Student_Output(Student_Base):
    student_id: int
    class Config:
        from_attributes = True
