from sqlalchemy.orm import Session
from app.models import Video, Enrollment

def upload_video(db : Session, course_id : int, teacher_id : int, video_name : str, video_url : str, video_description : str, video_order_id : int, video_duration : int, video_preview_url : str):
    check_video = db.query(Video).filter(Video.course_id == course_id, Video.teacher_id == teacher_id, Video.video_url == video_url).first()

    if check_video:
        return check_video
    else:
        new_video = Video(teacher_id = teacher_id, course_id = course_id, video_name = video_name, video_url = video_url, video_order_id = video_order_id, video_description = video_description, video_duration = video_duration, video_preview_url = video_preview_url)
        db.add(new_video)
        db.commit()
        db.refresh(new_video)
        return new_video


def get_all_videos_from_course(db : Session, student_id : int, course_id : int, teacher_id : int):
    check_student = db.query(Enrollment).filter(Enrollment.course_id == course_id, Enrollment.student_id == student_id, Enrollment.teacher_id == teacher_id).first()
    if check_student:
        videos = db.query(Video).filter(Video.course_id == course_id, Video.teacher_id == teacher_id).order_by(Video.video_order_id).distinct().all()
        if videos:
            return videos
    

    return []


def get_video_for_teacher(db : Session, course_id : int, teacher_id : int, video_url : str):
    video = db.query(Video).filter(Video.course_id == course_id, Video.teacher_id == teacher_id, Video.video_url == video_url).first()
    if video:
        return video
    