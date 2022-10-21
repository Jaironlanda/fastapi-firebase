from pydantic import BaseModel


class SignupBase(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class UserProfile(BaseModel):
    email: str


