from sqlalchemy.orm import Session
from app.models import Progress


def upload_progress(db: Session, video_id: int, student_id: int, last_position: int):
    check_progress = (
        db.query(Progress)
        .filter(Progress.video_id == video_id, Progress.student_id == student_id)
        .first()
    )

    if check_progress:
        check_progress.last_position = last_position

        db.commit()
        return check_progress
    else:
        new_progress = Progress(
            video_id=video_id,
            student_id=student_id,
            is_watched=False,
            last_position=last_position,
        )
        db.add(new_progress)
        db.commit()
        db.refresh(new_progress)
        return new_progress
