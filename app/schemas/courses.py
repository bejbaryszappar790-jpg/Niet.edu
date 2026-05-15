from pydantic import BaseModel, Field


class Course_Base(BaseModel):
    course_name: str = Field(..., min_length = 1, max_length = 50)
    course_sphere: str = Field(..., min_length = 1, max_length = 50)


class Course_Registration(Course_Base):
    pass


class Output_Schema(Course_Base):
    course_id: int

    class Config:
        from_attributes = True
