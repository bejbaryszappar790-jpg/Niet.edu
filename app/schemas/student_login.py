from pydantic import BaseModel, EmailStr, Field


class Student_Login_Input(BaseModel):
    student_plain_password : str = Field(..., min_length = 8)
    student_email : EmailStr
