from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.token import Refresh_Token_Input, Token_Base
from app.core.security import create_refresh_token, create_access_token, decode_refresh_token


router = APIRouter(prefix = "/authentication", tags = ["Get_token"])

@router.post("/new_token", response_model = Token_Base)
def give_user_token(refresh_token_in : Refresh_Token_Input,  db : Session = Depends(get_db)):
    payload = decode_refresh_token(refresh_token_in.refresh_token)
    
    user_id = payload.get("sub")
    
    refresh_data = {"sub": str(user_id)}
    access_data = {"sub" : str(user_id)}
    
    refresh_token = create_refresh_token(data = refresh_data, role = payload.get("role"))
    access_token = create_access_token(data = access_data, role = payload.get("role"))

    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "token_type" : "bearer"
    }
    
    