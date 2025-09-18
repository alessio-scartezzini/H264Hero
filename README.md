# H264Hero

H264Hero is a Python utility that automatically converts videos to **MP4 with H.264 video and AAC audio**. It intelligently detects available hardware acceleration (Intel, NVIDIA, AMD) for faster processing, skips already compatible files, and ensures smooth, streaming-ready output with minimal effort.

---

## Features

- ✅ Converts virtually any video format (`.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.ts`, `.webm`, `.mp4`) to **MP4 H.264 + AAC**  
- ✅ Detects **hardware acceleration**: Intel QuickSync, NVIDIA NVENC, AMD AMF  
- ✅ Skips videos already encoded in H.264 + AAC  
- ✅ Allows **single file, multiple files, or full folder batch conversion**  
- ✅ Adds `_converted` suffix to output files to prevent overwriting originals  
- ✅ Optimized for **fast streaming** with `+faststart` flag  
- ✅ All corrected converted video will be in a folder called "converted"
- ✅ The one who fails will keep the original file only

---

## Installation

1. Make sure **Python 3** is installed  
2. Make sure **FFmpeg** is installed and available in your system PATH  
3. Clone or download this repository:  
```bash
git clone https://github.com/alessio-scartezzini/H264Hero.git
cd H264Hero
```

4. Run the script:  
```bash
python3 h264hero.py
```

---

## Usage

When you run the script, you'll see three options:

1. **Convert a single file**  
   Enter the path to your video file  
   The script will convert it to MP4 H.264 + AAC if needed

2. **Convert multiple selected files**  
   Enter the paths of multiple video files separated by commas

3. **Convert all videos in a folder**  
   Enter the folder path  
   The script will process all supported video files in that folder

The output files will have `_converted` appended to their names

---

## How It Works

- **Hardware Detection**  
  The script runs `ffmpeg -encoders` to check which GPU encoders are available  
  It uses the best available encoder for faster conversion

- **File Checking**  
  For MP4 files, it checks if the video stream is already H.264  
  If yes, the file is skipped

- **Conversion Command**  
  Uses FFmpeg with the selected encoder, `-preset fast`, AAC audio, and `+faststart` for streaming optimization  
  Errors during conversion are logged in the console

---

## Supported Video Extensions

```
.avi, .mkv, .mov, .wmv, .flv, .ts, .webm, .mp4
```

---

## Notes & Tips

- Make sure FFmpeg is up to date for best compatibility
- For Intel QuickSync, the `-hwaccel qsv` flag is automatically used
- Output files are not overwritten; originals remain untouched
- Batch conversion can be slow depending on file sizes and hardware; GPU acceleration can drastically speed up the process
- Works on Windows, Linux, and macOS, as long as Python and FFmpeg are installed

---

## License

H264Hero is licensed under GNU GPLv3 with an additional Non-Commercial clause:

- ✅ You can use, modify, and redistribute it for free
- ❌ You cannot sell or distribute it for commercial purposes
- 🔄 Any modifications must be shared under the same terms

See `LICENSE` and `LICENSE-NC` files for full details.
