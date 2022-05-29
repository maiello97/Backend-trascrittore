import datetime
from pydantic import BaseModel


class User(BaseModel):
    id:int
    username:str
    password:str

    class Config:
        orm_mode=True

class CreateLogin(BaseModel):
    username:str
    password:str

class Trascrizione(BaseModel): 
    id:int
    audio:str
    trascrizione:str
    data:str

    class Config:
        orm_mode=True

class CreateTrascrizione(BaseModel): 
    audio:str
    trascrizione:str
    data:str