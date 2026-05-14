from pydantic import BaseModel, EmailStr, Field

class Teacher_Input_Login(BaseModel):
    teacher_plain_password : str = Field(..., min_length = 8)
    teacher_email : EmailStr