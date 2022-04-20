from typing import Optional
import wave

from fastapi import FastAPI, UploadFile,Form
from starlette.middleware.cors import CORSMiddleware
from services import get_transcription






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
async def create_upload_file(file: UploadFile = Form(...), url: str = Form(...)):

    

    """res = get_transcription(url)"""    


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