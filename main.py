from ast import For
from datetime import date, datetime
from http.client import HTTPException
from typing import List, Optional
from urllib import response
import wave

from fastapi import FastAPI, UploadFile,Form, Depends
from grpc import services
from starlette.middleware.cors import CORSMiddleware
from services import get_transcription, auth_user, createuser, get_user_by_email, addTrascription

import fastapi.security as security
from db import SessionLocal, engine 
from sqlalchemy.orm import Session
import db as database, models, schemas

import os.path

from datetime import date
import time



models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = Form(...), url: str = Form(...), data:str = Form(...), state:str = Form(...), db:Session=Depends(get_db)):

    nchannels = 2
    sampwidth = 2
    framerate = 28000
    nframes = 1600
  
    name = date.today().strftime("%d-%m-%Y")+"-"+time.strftime("%H_%M_%S")

    audio = wave.open("Temp/"+name+".wav", 'wb')
    audio.setnchannels(nchannels)
    audio.setsampwidth(sampwidth)
    audio.setframerate(framerate)
    audio.setnframes(nframes)
    
    audio.writeframes(file.file.read())
             
    res = get_transcription(name)

    if state == "false" :
        await addTrascription(file.filename, res, data, db)
    return res


@app.post("/login")
async def autentication(form_data:security.OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = await auth_user(form_data.username, form_data.password, db)
    if not user: 
        raise HTTPException(status_code=401, detail="Credenziali non valide")
    response = True 

    return response

@app.post("/login/createuser")
async def create_user(user:schemas.CreateLogin, db:Session = Depends(get_db)): 
    db_user = await get_user_by_email(user.username, db)

    if db_user:
        raise HTTPException(status_code=400, detail="Utente già esistente")
    user = await createuser(user, db)
    return user

@app.get("/users/all", response_model=List[schemas.User])
async def getAllUsers(db:Session= Depends(get_db)):
    response = db.query(models.User).all()
    return response