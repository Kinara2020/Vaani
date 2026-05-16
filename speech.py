import whisper
import sounddevice as sd
import numpy as np

model = whisper.load_model("base")

SAMPLE_RATE = 16000
CHUNK_DURATION = 4

def record_chunk():
    print("Recording...")
    audio = sd.rec(
        int(CHUNK_DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )
    sd.wait()
    return audio.flatten()

def transcribe_chunk(audio_np):
    try:
        result = model.transcribe(audio_np, fp16=False, language='en')
        return result['text'].strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""

def start_listening(callback):
    print("Listening started...")
    while True:
        audio = record_chunk()
        text = transcribe_chunk(audio)
        if text:
            print(f"Transcribed: {text}")
            callback(text)