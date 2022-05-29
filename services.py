from datetime import date
from requests import session
import torch
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from transformers.tokenization_utils_base import BatchEncoding

import db as database, models, schemas
from db import SessionLocal, engine 
import sqlalchemy.orm as orm
import bcrypt
batch = BatchEncoding({"inputs": [[1, 2, 3], [4, 5, 6]], "labels": [0, 1]})
tensor_batch = batch.convert_to_tensors(tensor_type="pt",prepend_batch_axis=True)

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-xlsr-53-italian")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53-italian")


def get_db():
    try:
        db= SessionLocal()
        yield db
    finally:
        db.close()


def get_transcription():
    audio_input, rate = librosa.load("Temp/output.wav")
    audio_input = librosa.resample(audio_input.T, rate, 16000)
    audio_input = tokenizer(audio_input, return_tensors="pt", padding=True).input_values.unsqueeze(0) #added unsqueeze(0) for recording from microphone here
    logits = model(audio_input[0]).logits
    predicted_ids = torch.argmax(input = logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]
    return transcription


async def get_user_by_email(email:str, db:orm.Session):
    return db.query(models.User).filter(models.User.username == email).first()


async def auth_user(email:str, password:str, db:orm.Session):
    user = await get_user_by_email(email, db)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

async def createuser(user: schemas.CreateLogin, db:orm.Session):
    password = user.password.encode('utf-8')
    user_obj = models.User(username = user.username, password = bcrypt.hashpw(password, bcrypt.gensalt()))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def addTrascription(file:str, trascription:str, date:date, db:orm.Session):
    trascription_obj = models.Trascrizione(audio = file, trascrizione = trascription, data = date)
    db.add(trascription_obj)
    db.commit()
    db.refresh(trascription_obj)