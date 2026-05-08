from pydantic import BaseModel, EmailStr, Field


class Course_Base(BaseModel):
    course_name: str = Field(..., min_length = 1, max_length = 50)
    course_sphere: str = Field(..., min_length = 1, max_length = 50)


class Course_Registration(Course_Base):
    teacher_email: EmailStr
    teacher_password: str = Field(..., min_length = 8)


class Output_Schema(Course_Base):
    course_id: int

    class Config:
        from_attributes = True
