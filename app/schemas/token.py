from pydantic import BaseModel


class Token_Base(BaseModel):
    access_token: str
    refresh_token : str
    token_type : str
    class Config:
        from_attributes = True


class Refresh_Token_Input(BaseModel):
    refresh_token : str
    