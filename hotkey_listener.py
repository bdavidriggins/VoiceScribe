"""
Voice-to-Text Transcription with Automatic Text Insertion
----------------------------------------------------------
This Python script is designed to run as a background service that listens for
a global hotkey (Shift + Windows key). When both keys are pressed together,
the script records audio from the microphone, transcribes it using OpenAI's
Whisper model, and inserts the transcribed text at the cursor's current 
position in the active application on Ubuntu Linux.

Dependencies:
    - sounddevice: for recording audio
    - whisper: OpenAI's model for transcription
    - pynput: for detecting hotkey presses
    - numpy: for handling audio data
    - subprocess: for executing system commands (xdotool)
    - logging: for logging events and errors

Main Components:
    1. Hotkey Listener: Detects when Shift and Windows keys are pressed.
    2. Audio Recorder: Captures microphone input when hotkey is pressed.
    3. Transcription: Uses Whisper to transcribe the recorded audio.
    4. Text Inserter: Inserts the transcribed text at the current cursor position using xdotool.

Instructions:
    Run this script, and it will continuously listen for the hotkey combination. 
    When detected, the script records your speech and types the transcribed 
    text into the active application.

Note: Ensure that xdotool is installed on your system for text insertion.
"""

import sounddevice as sd
import numpy as np
import whisper
from pynput import keyboard
import threading
import subprocess
import logging

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO,  # Set the base logging level
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
                    handlers=[logging.StreamHandler()])  # Console logging

# Load the Whisper model for transcription
try:
    model = whisper.load_model("base.en")
    logging.info("Whisper model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load Whisper model: {e}", exc_info=True)
    raise

# Sampling frequency for audio recording
fs = 16000

# Global variables
is_recording = False  # Flag to indicate if recording is active
audio_frames = []  # To store recorded audio data
current_keys = set()  # Track currently pressed keys for hotkey detection

def audio_callback(indata, frames, time, status):
    """
    Callback function to handle incoming audio data during recording.
    Appends the audio data to the global `audio_frames` list.
    """
    try:
        if status:
            logging.warning(f"Audio callback status: {status}")
        audio_frames.append(indata.copy())
    except Exception as e:
        logging.error(f"Error in audio_callback: {e}", exc_info=True)

def start_recording():
    """
    Starts recording audio using the sounddevice library. Runs in a separate
    thread and continues recording while the `is_recording` flag is True.
    """
    global audio_frames
    audio_frames = []  # Clear any previous audio data

    try:
        # Open an audio stream to capture input from the microphone
        with sd.InputStream(samplerate=fs, channels=1, callback=audio_callback):
            while is_recording:
                sd.sleep(100)
    except Exception as e:
        logging.error(f"Error during audio recording: {e}", exc_info=True)

def on_press(key):
    """
    Callback function triggered when any key is pressed. Checks if the
    Shift and Windows keys are pressed to start recording.
    """
    global is_recording
    try:
        # Add the key to the set if it's Shift or Windows
        if key in (keyboard.Key.shift_l, keyboard.Key.shift_r, keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r):
            current_keys.add(key)
            logging.debug(f"Key pressed: {key}")

        # If both Shift and Windows keys are pressed, start recording
        if (keyboard.Key.shift_l in current_keys or keyboard.Key.shift_r in current_keys) and \
           (keyboard.Key.cmd in current_keys or keyboard.Key.cmd_l in current_keys or keyboard.Key.cmd_r in current_keys):
            if not is_recording:
                is_recording = True
                logging.info("Recording started.")
                # Start recording in a new thread to avoid blocking the main thread
                threading.Thread(target=start_recording, daemon=True).start()
    except Exception as e:
        logging.error(f"Error in on_press: {e}", exc_info=True)

def on_release(key):
    """
    Callback function triggered when any key is released. Stops recording
    and initiates transcription when both Shift and Windows keys are released.
    """
    global is_recording
    try:
        # Remove the key from the set if it's Shift or Windows
        if key in (keyboard.Key.shift_l, keyboard.Key.shift_r, keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r):
            current_keys.discard(key)
            logging.debug(f"Key released: {key}")

        # If neither Shift nor Windows key is pressed, stop recording and transcribe audio
        if is_recording and not any(k in current_keys for k in (keyboard.Key.shift_l, keyboard.Key.shift_r, keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r)):
            is_recording = False
            logging.info("Recording stopped.")

            # Ensure audio was recorded before transcribing
            if audio_frames:
                try:
                    # Process and transcribe the recorded audio
                    audio_data = np.concatenate(audio_frames, axis=0)
                    audio_data = np.squeeze(audio_data)
                    logging.info("Transcribing audio...")
                    result = model.transcribe(audio_data, language='en')
                    transcribed_text = result['text']
                    logging.info(f"Transcribed Text: {transcribed_text}")
                    # Insert the transcribed text at the current cursor position
                    insert_text(transcribed_text)
                except Exception as e:
                    logging.error(f"Error during transcription or text insertion: {e}", exc_info=True)
            else:
                logging.info("No audio data recorded.")
    except Exception as e:
        logging.error(f"Error in on_release: {e}", exc_info=True)

def insert_text(text):
    """
    Uses xdotool to simulate typing of the transcribed text into the active application.
    """
    try:
        result = subprocess.run(['xdotool', 'type', '--clearmodifiers', text], check=True)
        logging.info("Text inserted successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to insert text using xdotool: {e}", exc_info=True)
    except Exception as e:
        logging.error(f"Unexpected error in insert_text: {e}", exc_info=True)

def main():
    """
    Main function that starts the hotkey listener and runs indefinitely to detect hotkey presses.
    """
    logging.info("Voice transcription application started. Press Shift + Windows key to record.")
    try:
        # Start the keyboard listener to detect hotkey presses/releases
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()  # Keep the listener running until manually interrupted
    except Exception as e:
        logging.error(f"Error in main listener: {e}", exc_info=True)

# Entry point of the script
if __name__ == "__main__":
    main()
