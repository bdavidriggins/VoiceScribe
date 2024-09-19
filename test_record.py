import sounddevice as sd
import numpy as np
import whisper

# Initialize Whisper model
model = whisper.load_model("base.en")

fs = 16000  # Sampling frequency
duration = 5  # Duration in seconds

print("Recording...")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.float32)
sd.wait()
print("Recording complete. Transcribing...")

# Preprocess and transcribe
audio = np.squeeze(audio)
result = model.transcribe(audio, language='en')
transcribed_text = result['text']

print("Transcribed Text:", transcribed_text)
