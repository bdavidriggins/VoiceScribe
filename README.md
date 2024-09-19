```markdown
# Voice Transcribe

Effortless speech-to-text transcription for Ubuntu desktop.

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
  - [Conda Virtual Environment](#conda-virtual-environment)
  - [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Additional Resources](#additional-resources)

---

## Features

- **Global Hotkey**: Trigger transcription with a customizable hotkey combination (Windows key + Shift).
- **Accurate Speech Recognition**: Powered by OpenAI's Whisper model for high-quality transcription.
- **Automatic Text Insertion**: Transcribed text is automatically inserted into any active application.
- **Ubuntu Desktop Integration**: Seamlessly integrates with the Ubuntu desktop environment.
- **Background Service**: Runs continuously in the background.
- **Development and Deployment**: Uses Conda for development environment and Docker for deployment.

## System Architecture

The application consists of the following components:

1. **Background Service**: Runs continuously, listening for the global hotkey.
2. **Hotkey Listener**: Detects when the user presses and releases the specified key combination.
3. **Audio Recorder**: Records audio input from the microphone during the hotkey press.
4. **Transcription Module**: Uses Whisper to transcribe the recorded audio.
5. **Text Inserter**: Simulates keyboard input to insert the transcribed text at the cursor's position.
6. **System Integration**: Ensures the application starts automatically and has the necessary permissions.

**Flow Diagram:**

```
[User Presses Hotkey]
         ↓
[Audio Recording Starts]
         ↓
[User Releases Hotkey]
         ↓
[Audio Recording Stops]
         ↓
    [Transcription Module]
         ↓
     [Text Inserter]
         ↓
[Transcribed Text Inserted at Cursor Position]
```

## Getting Started

### Prerequisites

- **Ubuntu Linux**: The application is designed for Ubuntu desktop environments.
- **Microphone**: For capturing audio input.
- **X11 Display Server**: Required for keyboard emulation.
- **Conda**: For managing the virtual environment (Miniconda or Anaconda).
- **Docker**: For containerization (optional, for deployment).

### Installation

#### Clone the Repository

```bash
git clone https://github.com/your-username/voice-transcribe.git
cd voice_transcribe
```

#### Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y xdotool libportaudio2
```

#### Set Up Conda Virtual Environment

Install Conda (if not already installed):

```bash
# Download Miniconda installer for Linux
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Create and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate voice_transcribe
```

#### Install Whisper Model

```bash
pip install git+https://github.com/openai/whisper.git
```

#### Run the Application

```bash
python main.py  # Replace 'main.py' with the actual script name
```

## Usage

- **Start the Application**: Ensure the background service is running.
- **Trigger Transcription**: Press and hold the global hotkey (Windows key + Shift) to start recording.
- **Stop Recording**: Release the hotkey to stop recording and automatically insert the transcribed text into the active application.

## Development

### Conda Virtual Environment

We use a Conda virtual environment to manage project dependencies and isolate the development environment.

- **Create and Activate Environment**:

  ```bash
  conda env create -f environment.yml
  conda activate voice_transcribe
  ```

- **Environment Configuration** (`environment.yml`):

  ```yaml
  name: voice_transcribe
  channels:
    - defaults
  dependencies:
    - python=3.9
    - numpy
    - pip
    - pip:
        - sounddevice
        - whisper
        - pynput
        - pyautogui
        - pyperclip
  ```

### Docker Deployment

To ensure a consistent deployment environment, we provide a Dockerfile for containerization.

#### Build the Docker Image

```bash
docker build -t voice_transcribe:latest .
```

#### Run the Docker Container

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

**Note**: The `--privileged` flag is required to access input devices and simulate keyboard events from within the container. Use it cautiously due to potential security risks.

#### Troubleshooting

- **Audio Issues**: Ensure that the container has access to `/dev/snd` and verify PulseAudio settings.
- **Display Issues**: Confirm that X11 sockets are correctly mounted and the `DISPLAY` environment variable is set.
- **Permission Errors**: Running the container with `--privileged` may be necessary. Alternatively, set specific device permissions.

## Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository.
2. **Create** a new branch (`git checkout -b feature/YourFeature`).
3. **Commit** your changes (`git commit -m 'Add some feature'`).
4. **Push** to the branch (`git push origin feature/YourFeature`).
5. **Open** a Pull Request.

Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- **Whisper Model**: This project uses the [Whisper](https://github.com/openai/whisper) model for speech recognition, developed by OpenAI.
- **pynput**: For global hotkey detection.
- **sounddevice**: For audio recording.
- **xdotool**: For simulating keyboard input.
- **pyautogui**: For automating GUI interactions.

## Additional Resources

- **Project Design Document**: Detailed design and implementation plan can be found in [docs/DesignDocument.md](docs/DesignDocument.md).
- **Change Log**: See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

Feel free to replace `your-username` with your actual GitHub username, and `main.py` with the actual script name. Make sure to update the `LICENSE` file with the appropriate license information.

**Note**: Ensure thorough testing of the Dockerized application, especially concerning permissions and access to host resources like audio devices and input events.

### Security Considerations

- **Priv