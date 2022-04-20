import torch
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

from transformers.tokenization_utils_base import BatchEncoding

batch = BatchEncoding({"inputs": [[1, 2, 3], [4, 5, 6]], "labels": [0, 1]})
tensor_batch = batch.convert_to_tensors(tensor_type="pt",prepend_batch_axis=True)

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-xlsr-53-italian")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53-italian")


def get_transcription():
    audio_input, rate = librosa.load("Temp/output.wav")
    audio_input = librosa.resample(audio_input.T, rate, 16000)
    audio_input = tokenizer(audio_input, return_tensors="pt", padding=True).input_values.unsqueeze(0) #added unsqueeze(0) for recording from microphone here
    logits = model(audio_input[0]).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]
    return transcription

