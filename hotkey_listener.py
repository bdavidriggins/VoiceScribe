import sounddevice as sd
import numpy as np
import whisper
from pynput import keyboard
import threading
import subprocess
import logging

model = whisper.load_model("base.en")
fs = 16000
is_recording = False
audio_frames = []
current_keys = set()
logging.basicConfig(level=logging.INFO)


def audio_callback(indata, frames, time, status):
    audio_frames.append(indata.copy())

def start_recording():
    global audio_frames
    audio_frames = []
    with sd.InputStream(samplerate=fs, channels=1, callback=audio_callback):
        while is_recording:
            sd.sleep(100)

def on_press(key):
    global is_recording
    try:
        if key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            current_keys.add(key)
        if key == keyboard.Key.cmd:
            current_keys.add(key)

        # Check if both Shift and Windows keys are pressed
        if keyboard.Key.shift_l in current_keys or keyboard.Key.shift_r in current_keys:
            if keyboard.Key.cmd in current_keys and not is_recording:
                if not is_recording:
                    is_recording = True
                    threading.Thread(target=start_recording).start()
    except AttributeError:
        pass

def on_release(key):
    global is_recording
    try:
        if key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            current_keys.discard(key)
        if key == keyboard.Key.cmd:
            current_keys.discard(key)



        # Stop recording if no longer pressing both keys
        if is_recording and (keyboard.Key.shift_l not in current_keys and 
                             keyboard.Key.shift_r not in current_keys and 
                             keyboard.Key.cmd not in current_keys):
            if is_recording:
                is_recording = False
                # Check if audio_frames is not empty before concatenating
                if audio_frames:
                    # Process audio
                    audio_data = np.concatenate(audio_frames, axis=0)
                    audio_data = np.squeeze(audio_data)
                    result = model.transcribe(audio_data, language='en')
                    transcribed_text = result['text']
                    logging.info("Transcribed Text:", transcribed_text)
                    insert_text(transcribed_text)
                else:
                    logging.info("No audio data recorded.")
    except AttributeError:
        pass


def insert_text(text):
    subprocess.run(['xdotool', 'type', '--clearmodifiers', text])


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
