from pydantic import BaseModel, EmailStr, Field


class Teacher_Base(BaseModel):
    teacher_first_name: str = Field(..., min_length = 1, max_length = 50)
    teacher_last_name: str = Field(..., min_length = 1, max_length = 50)


class Teacher_Registration(Teacher_Base):
    teacher_email: EmailStr 
    teacher_plain_password: str = Field(..., min_length = 8)


class Teacher_Output(Teacher_Base):
    teacher_id: int

    class Config:
        from_attributes = True
