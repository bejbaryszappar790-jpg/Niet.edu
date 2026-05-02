from pydantic import BaseModel
from datetime import datetime 

class Progress_Base(BaseModel):
    student_id : int
    video_id : int
    watched_on : datetime | None
    is_watched : bool


class Progress_Input(Progress_Base):
    last_position : int
    
class Progress_Output(Progress_Base):
    
    class Config:
        progress_id : int
        from_attributes = True