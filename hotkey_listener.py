import sounddevice as sd
import numpy as np
import whisper
from pynput import keyboard
import threading
import subprocess
import logging



logging.basicConfig(level=logging.INFO,  # Set the base logging level
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
                    handlers=[logging.StreamHandler()])  # Console logging

try:
    model = whisper.load_model("base.en")
    logging.info("Whisper model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load Whisper model: {e}", exc_info=True)
    raise

# Sampling frequency
fs = 16000

# Global variables
is_recording = False
audio_frames = []
current_keys = set()



def audio_callback(indata, frames, time, status):
    try:
        if status:
            logging.warning(f"Audio callback status: {status}")
        audio_frames.append(indata.copy())
    except Exception as e:
        logging.error(f"Error in audio_callback: {e}", exc_info=True)

def start_recording():
    global audio_frames
    audio_frames = []

    try:
        with sd.InputStream(samplerate=fs, channels=1, callback=audio_callback):
            while is_recording:
                sd.sleep(100)
    except Exception as e:
        logging.error(f"Error during audio recording: {e}", exc_info=True)


def on_press(key):
    global is_recording
    try:
        # Add key to current_keys set if it's Shift or Windows key
        if key in (keyboard.Key.shift_l, keyboard.Key.shift_r, keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r):
            current_keys.add(key)
            logging.debug(f"Key pressed: {key}")

        # Check if both Shift and Windows keys are pressed
        if (keyboard.Key.shift_l in current_keys or keyboard.Key.shift_r in current_keys) and \
           (keyboard.Key.cmd in current_keys or keyboard.Key.cmd_l in current_keys or keyboard.Key.cmd_r in current_keys):
            if not is_recording:
                is_recording = True
                logging.info("Recording started.")
                threading.Thread(target=start_recording, daemon=True).start()

    except Exception as e:
        logging.error(f"Error in on_press: {e}", exc_info=True)

def on_release(key):
    global is_recording
    try:
        # Remove key from current_keys set if it's Shift or Windows key
        if key in (keyboard.Key.shift_l, keyboard.Key.shift_r, keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r):
            current_keys.discard(key)
            logging.debug(f"Key released: {key}")

        # Stop recording if neither Shift nor Windows key is pressed
        if is_recording and not any(k in current_keys for k in (keyboard.Key.shift_l, keyboard.Key.shift_r, keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r)):
            is_recording = False
            logging.info("Recording stopped.")

            # Check if audio_frames is not empty before processing
            if audio_frames:
                try:
                    # Process audio
                    audio_data = np.concatenate(audio_frames, axis=0)
                    audio_data = np.squeeze(audio_data)
                    logging.info("Transcribing audio...")
                    result = model.transcribe(audio_data, language='en')
                    transcribed_text = result['text']
                    logging.info(f"Transcribed Text: {transcribed_text}")
                    insert_text(transcribed_text)
                except Exception as e:
                    logging.error(f"Error during transcription or text insertion: {e}", exc_info=True)
            else:
                logging.info("No audio data recorded.")
    except Exception as e:
        logging.error(f"Error in on_release: {e}", exc_info=True)


def insert_text(text):
    try:
        result = subprocess.run(['xdotool', 'type', '--clearmodifiers', text], check=True)
        logging.info("Text inserted successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to insert text using xdotool: {e}", exc_info=True)
    except Exception as e:
        logging.error(f"Unexpected error in insert_text: {e}", exc_info=True)


def main():
    logging.info("Voice transcription application started. Press Shift + Windows key to record.")
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        logging.error(f"Error in main listener: {e}", exc_info=True)

if __name__ == "__main__":
    main()