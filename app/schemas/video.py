from pydantic import BaseModel, HttpUrl

class Video_Base(BaseModel):
    video_name : str
    video_url : HttpUrl
    teacher_id : int
    video_order_id : int
    video_description : str


class Video_Upload(Video_Base):
    course_id : int

class Video_Output(Video_Base):
    video_id : int
    class Config:
        from_attributes = True