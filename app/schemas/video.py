from pydantic import BaseModel, HttpUrl

class Video_Base(BaseModel):
    video_name : str | None
    video_url : HttpUrl
    teacher_id : int
    course_id : int
    video_order_id : int
    video_description : str | None
    video_duration : int | None
    video_preview_url : HttpUrl | None


class Video_Upload(Video_Base):
    pass

class Video_Output(Video_Base):
    video_id : int
    youtube_id : str
    class Config:
        from_attributes = True