from io import BytesIO
from typing import Optional
import wave

from fastapi import FastAPI, File, UploadFile,HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from services import get_transcription
import shutil
import moviepy.editor as moviepy

import struct




app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):

    content = file.file.read()


    """with wave.open(file.filename, 'wb') as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(8000)
            audio.writeframesraw(content)"""
            
    res = get_transcription(content)

        
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT'
        },
        'body': res
    }