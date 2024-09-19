# Voice Transcribe

Effortless speech-to-text transcription for Ubuntu desktop.

## Overview

**Voice Transcribe** is a simple, keyboard-driven solution for transcribing spoken words to text. Powered by OpenAI's Whisper model for accurate speech recognition, this tool allows users to trigger transcription with a global hotkey, automatically inserting the transcribed text into any active application.

## Key Features

- **Global hotkey:** Trigger transcription with a customizable hotkey combination (Shift + Windows key by default).
- **Accurate speech recognition:** Powered by the Whisper model for high-quality transcription.
- **Automatic text insertion:** Transcribed text is automatically inserted into the active application at the current cursor position.
- **Ubuntu desktop integration:** Seamlessly integrates with the Ubuntu desktop environment.

## Getting Started

### Prerequisites

- **Ubuntu Linux** (Tested on Ubuntu Desktop)
- **Python 3.9+**
- **Conda** (for virtual environment management)
- **Docker** (optional, for containerized deployment)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/voice-transcribe.git
    cd voice-transcribe
    ```

2. **Set up Conda environment:**

    Install dependencies using the provided Conda environment:

    ```bash
    conda env create -f environment.yml
    conda activate voice_transcribe
    ```

3. **Install system dependencies:**

    Ensure `xdotool` is installed to allow text insertion:

    ```bash
    sudo apt-get install xdotool
    ```

4. **Run the application:**

    ```bash
    python hotkey_listener.py
    ```

    This will start the application, allowing it to listen for the hotkey combination and perform transcription.

### Docker Deployment (Optional)

You can also run the application in a Docker container:

1. **Build the Docker image:**

    ```bash
    docker build -t voice_transcribe:latest .
    ```

2. **Run the Docker container:**

    ```bash
    docker run -d \
      --name voice_transcribe \
      --device /dev/snd \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      -e DISPLAY=$DISPLAY \
      -v $XAUTHORITY:/root/.Xauthority \
      --network host \
      --privileged \
      voice_transcribe:latest
    ```

## Development Environment

- **Conda virtual environment:** Dependencies are managed with Conda for consistent development environments (see `environment.yml`).
- **Docker containerization:** The application can be containerized and deployed using Docker (see `Dockerfile`).

## Contributing

Contributions are welcome! Please see the `CONTRIBUTING.md` file for guidelines on how to contribute to this project.

## License

[Insert license information, e.g., MIT License]

## Acknowledgments

- **Whisper model:** This project uses the Whisper model for speech recognition, developed by OpenAI.

---

_Replace `your-username` with your GitHub username and update the script name or license information accordingly._
