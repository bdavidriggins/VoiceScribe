import sounddevice as sd
import numpy as np
import whisper

# Initialize the Whisper model (using base multilingual model or base.en for English-only)
model = whisper.load_model("base.en")  # Use "base" for multilingual model

# Function to record audio from the microphone
def record_audio(duration, fs=16000):
    print("Recording audio...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.float32)
    sd.wait()  # Wait until the recording is finished
    return np.squeeze(audio)

# Function to transcribe recorded audio
def transcribe_audio(audio):
    # Whisper expects audio in 16kHz, so we need to adjust sample rate if necessary
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(language="en", fp16=False)  # Set language to English
    result = whisper.decode(model, mel, options)
    return result.text

# Example usage
duration = 10  # Duration in seconds
audio = record_audio(duration)  # Record audio for 10 seconds
transcribed_text = transcribe_audio(audio)  # Transcribe the recorded audio
print("Transcribed Text:", transcribed_text)

