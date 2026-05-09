from sqlalchemy.orm import Session
from app.models import Progress, Video


def upload_progress(db: Session, video_id: int, student_id: int, last_position: int):
    temp_video = db.query(Video).filter(Video.video_id == video_id ).first()

    
    if temp_video:
        progress = (
            db.query(Progress)
            .filter(Progress.video_id == video_id, Progress.student_id == student_id)
            .first()
        )


        check_is_watched = last_position >= int(temp_video.video_duration * 0.95)

        if progress:
            progress.last_position = last_position

            if check_is_watched:
                progress.is_watched = True
    
        else:
         
         
            progress = Progress(
                video_id=video_id,
                student_id=student_id,
                is_watched=check_is_watched,
                last_position=last_position,
            )
            db.add(progress)
    
    
        db.commit()
        db.refresh(progress)
        return progress
