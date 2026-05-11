from pydantic import BaseModel, EmailStr, Field


class Student_Base(BaseModel):
    student_first_name: str = Field(..., min_length = 1, max_length = 50)
    student_last_name: str = Field(..., min_length = 1, max_length = 50)


class Student_Registration(Student_Base):
    student_email: EmailStr
    student_hashed_password: str = Field(..., min_length = 8)


class Student_Output(Student_Base):
    student_id: int

    class Config:
        from_attributes = True
