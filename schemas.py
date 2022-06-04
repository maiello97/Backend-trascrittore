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
    trascrizione:str
    data:str

    class Config:
        orm_mode=True

class CreateTrascrizione(BaseModel): 
    trascrizione:str
    data:str

class Audio(BaseModel):
    id_audio:int
    titolo:str
    id_trascrizione:int

    class Config:
        orm_mode=True

class CreateAudio(BaseModel): 
    titolo:str
    id_trascrizione:str
