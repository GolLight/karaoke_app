# Karaoke Video Generator

A web application that automatically generates karaoke videos from music files. The application separates vocals from instrumentals, transcribes lyrics, and creates a synchronized karaoke video with lyrics overlay.

## Features

- 🎵 Vocal and instrumental track separation using Deep Learning
- 🎤 Automatic lyrics transcription using OpenAI Whisper
- 🎨 Dynamic lyrics visualization
- 🎬 Automated karaoke video generation
- 🌐 Web interface for easy file upload

### Intelligent Vocal Detection

- Implements advanced audio analysis to precisely detect when vocals actually begin
- Uses decibel threshold detection (65dB) to identify the first vocal entry
- Automatically adjusts lyric timing by analyzing audio waveforms
- Pre-emptively displays lyrics 1 second before vocals start for better user experience
- Eliminates common issues with silence or instrumental intros in songs

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Audio Processing**:
  - Vocal Separation: Vocal Remover (Deep Learning based)
  - OpenAI Whisper (for transcription) (Transformer based)
  - Librosa
  - Soundfile
- **Image Processing**: Pillow (PIL)
- **Video Generation**: FFmpeg

## Installation

1. Clone the repository:
```bash
git clone https://github.com/saianish03/karaoke_app
cd karaoke-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg if not already installed:
- For Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)
- For Linux: `sudo apt-get install ffmpeg`
- For macOS: `brew install ffmpeg`

4. Install Vocal Separation Model:
- Follow Instructions from [vocal-remover](https://github.com/tsurumeso/vocal-remover)
- Clone the repository in the utils folder

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:8000` to upload a music file.

3. Upload an MP3 or WAV file through the web interface

4. The application will:
   - Separate vocals from instrumentals
   - Transcribe the lyrics
   - Generate synchronized lyric images
   - Create a karaoke video with the instrumental track

## Project Structure

├── README.md
└── src
    ├── README.md
    ├── app.py
    ├── main.py
    ├── processed_songs
    │   └── <song_name>/
    ├── songs
    │   └── <song_name>.mp3
    ├── static
    │   └── karaoke.css
    ├── templates
    │   ├── base.html
    │   └── index.html
    ├── test.ipynb
    └── utils
        ├── fonts/
        ├── image_to_video.py
        ├── text_to_images.py
        ├── utils.py
        └── vocal-remover/

## Processing Pipeline

1. **Vocal Separation**: Splits the input audio into vocal and instrumental tracks
2. **Transcription**: Uses Whisper to generate timestamped lyrics
3. **Timestamp Correction**: Adjusts timing for better synchronization
4. **Image Generation**: Creates styled lyric slides
5. **Audio Mixing**: Combines processed vocals with instrumentals
6. **Video Generation**: Produces the final karaoke video

## Supported File Formats

- Input: MP3, WAV
- Output: MP4 (karaoke video)