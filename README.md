# TikTok & YouTube Audio Downloader

A simple PyQt6 desktop app to download audio from TikTok or YouTube videos as MP3.  
Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp) for fast and reliable downloads.

## Features
- Download audio from TikTok or YouTube links
- Save files as MP3
- Simple PyQt6 GUI
- Progress bar during download
- Choose any folder for saving files

## Requirements
- Python 3.8 or higher
- yt-dlp
- PyQt6

Install dependencies:
```bash
pip install yt-dlp PyQt6
```

## Installation
1. Download the source code.  
2. Download ffmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).  
3. Extract ffmpeg and copy the three files from its `bin` folder:  
   - `ffmpeg`  
   - `ffprobe`  
   - `ffplay`  
   into the same folder as `audio_downloader.py`.  
4. Run the program:
```bash
python audio_downloader.py
```

## Usage
1. Paste a TikTok or YouTube video link  
2. Choose a save folder  
3. Click "Download Audio"  
4. Wait for the progress bar to finish — the MP3 file will be saved

## License
MIT License — free to use, modify, and share.
