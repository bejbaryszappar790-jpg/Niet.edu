from pydantic import BaseModel


class Video_Base(BaseModel):
    video_name: str | None
    video_url: str
    teacher_id: int
    course_id: int
    video_order_id: int
    video_description: str | None


class Video_Upload(Video_Base):
    pass


class Video_Output(Video_Base):
    video_id: int
    youtube_id: str
    video_duration: int
    video_preview_url: str | None
    class Config:
        from_attributes = True
