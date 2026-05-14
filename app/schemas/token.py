from pydantic import BaseModel


class Token_Base(BaseModel):
    access_token: str
    token_type : str
    class Config:
        from_attributes = True