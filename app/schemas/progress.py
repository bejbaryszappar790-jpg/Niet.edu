from pydantic import BaseModel
from datetime import datetime


class Progress_Base(BaseModel):
    student_id: int
    video_id: int
    last_position : int

class Progress_Input(Progress_Base):
    pass


class Progress_Output(Progress_Base):
    progress_id : int
    watched_on: datetime
    is_watched: bool
    class Config:
        from_attributes = True
