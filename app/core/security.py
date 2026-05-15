from jose import (
    jwt,
    JWTError,
)
from passlib.context import CryptContext
from datetime import (
    datetime,
    timedelta,
    timezone
)
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.student import get_student
from app.crud.teacher import get_teacher
from app.database import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCES_TIME = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TIME = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def get_password_hash(password : str):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(plain_password : str, hashed_password : str):
    result_of_checking = pwd_context.verify(plain_password, hashed_password)
    return result_of_checking

def create_access_token(data: dict, role : str):
    to_encode = data.copy()
    expire = datetime.now(timezone.UTC) + timedelta(minutes = ACCES_TIME)
    to_encode.update({"exp" : expire, "type" : "access", "role" : role})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, role : str):
    to_encode = data.copy()
    expire = datetime.now(timezone.UTC) + timedelta(days = REFRESH_TIME)
    to_encode.update({"exp" : expire, "type" : "refresh", "role" : role})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="students/student_login")

def get_current_user(token : str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        
        user_id = payload.get("sub")
        
        if user_id is None or not str(user_id).isdigit():
            raise HTTPException(status_code = 401, detail = "Could not validate credentials")

        return int(user_id)
    
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code = 401, detail = "Token is invalid or expired")
    
def decode_refresh_token(token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        
        if payload is None:
            raise HTTPException(status_code = 401, detail = "Token is invalid or expired")
        
        if payload.get("type") != "refresh":
            raise HTTPException(status_code = 401, detail = "Refresh token is required")
        
        return payload
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code = 401, detail = "Token is invalid or expired")
    


def get_current_student(student_id : int = Depends(get_current_user), db : Session = Depends(get_db)):
    check_student = get_student(db = db, student_id = student_id)

    if check_student:
        return check_student
    
    raise HTTPException(status_code = 403, detail = "Teacher is not allowed to use student's service for")

def get_current_teacher(teacher_id : int = Depends(get_current_user), db : Session = Depends(get_db)):
    check_teacher = get_teacher(db = db, teacher_id = teacher_id)
    
    if check_teacher:
        return check_teacher
    
    raise HTTPException(status_code = 403, detail = "Student is not allowed to use teacher's service for")