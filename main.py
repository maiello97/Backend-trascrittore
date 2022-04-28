from http.client import HTTPException
from typing import Optional
import wave

from fastapi import FastAPI, UploadFile,Form, Depends
from grpc import services
from starlette.middleware.cors import CORSMiddleware
from services import get_transcription, auth_user, createuser, get_user_by_email

import fastapi.security as security
from db import SessionLocal, engine 
from sqlalchemy.orm import Session
import db as database, models, schemas


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
async def create_upload_file(file: UploadFile = Form(...), url: str = Form(...)):

    nchannels = 2
    sampwidth = 2
    framerate = 28000
    nframes = 1600
  
    audio = wave.open("Temp/output.wav", 'wb')
    audio.setnchannels(nchannels)
    audio.setsampwidth(sampwidth)
    audio.setframerate(framerate)
    audio.setnframes(nframes)
    
    audio.writeframes(file.file.read())
             
    res = get_transcription()

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