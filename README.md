# Doom Sroll Detector 💤🚨

A Python-based computer vision project that monitors your webcam feed to detect if you fall asleep at your desk. It calculates the Eye Aspect Ratio (EAR) using AI facial landmarks and triggers an audio alarm to wake you up if your eyes stay closed for too long.

---

## Demo

> *TBA*

---

## Features

- **Real-Time Eye Tracking** — Uses Google's MediaPipe Face Mesh to track 478 3D facial landmarks and compute the EAR (Eye Aspect Ratio) for both eyes on every frame
- **Smart Alarm System** — Plays a looping audio alarm via Pygame when eyes have been closed past the threshold; automatically stops the moment you wake up
- **Audio Fallback Chain** — If Pygame or the sound file is missing, falls back to a motherboard system beep so the alarm always fires
- **Visual HUD Overlay** — Displays a live status pill (AWAKE / SLEEPING), real-time EAR value, eye-closure progress bar, and a pulsing red screen flash when the alarm triggers
- **Face Bounding Box** — Draws a styled corner-bracket box around your face, color-coded green (awake) or red (sleeping)
- **Dynamic File Pathing** — The alarm sound file is resolved relative to the script's location, so the project works from any folder or machine without hardcoded paths
- **Easily Configurable** — Two constants at the top of the file control everything:
  ```python
  EAR_THRESHOLD = 0.22      # How closed = "asleep"
  EYE_CLOSED_SECONDS = 2.5  # How long before alarm fires
  ```

---

## How It Works

1. OpenCV captures your webcam feed frame by frame
2. MediaPipe Face Mesh detects your face and returns 478 landmark coordinates
3. 6 specific landmarks around each eye are used to calculate the EAR using this formula:

```
EAR = (‖p2−p6‖ + ‖p3−p5‖) / (2 × ‖p1−p4‖)
```

When your eye is open, the EAR is typically `0.25–0.30`. When closed, it drops below `0.22`. If it stays below the threshold for more than 2.5 seconds, the alarm fires.

---

## Requirements

- Python **3.11** (recommended; 3.9–3.11 supported)
- A working webcam
- Windows / macOS / Linux

---

## Installation & Setup

**1. Clone the repository:**
```bash
git clone https://github.com/<your-username>/sleep-detect-alarm.git
cd sleep-detect-alarm
```

**2. Install dependencies:**
```bash
pip install mediapipe==0.10.14 opencv-python==4.10.0.84 numpy==1.26.4 matplotlib==3.8.4 pygame-ce
```

> ⚠️ **Important:** Use these exact versions. MediaPipe has strict compatibility requirements with NumPy and matplotlib. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for details.

**3. Add your alarm sound:**

Place any `.mp3` file named `drama-queen-alarm.mp3` in the project folder, or change this line in the script to match your file name:
```python
ALARM_SOUND_PATH = r"drama-queen-alarm.mp3"
```

**4. Run the script:**
```bash
python sleep-alarm.py
```

Press **Q** (with the webcam window focused) to quit.

---

## Webcam Troubleshooting

If you see `[ERROR] Cannot open webcam`, your camera index may be wrong. Change this line:
```python
cap = cv2.VideoCapture(0)  # Try 0, 1, or 2
```

To find your correct index automatically:
```python
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera found at index {i}")
        cap.release()
```

---

## Project Structure

```
sleep-detect-alarm/
├── sleep-alarm.py           # Main script
├── drama-queen-alarm.mp3    # Alarm sound file
├── requirements.txt         # Dependency list
├── README.md                # This file
└── TROUBLESHOOTING.md       # Full setup & error fix guide
```

---

## How to Record a Demo

The best demo for a computer vision project is a short GIF. Here's the easiest way to make one:

1. Download [ScreenToGif](https://www.screentogif.com/) (free, Windows)
2. Run your script: `python sleep-alarm.py`
3. Record a 5–10 second clip showing:
   - The AWAKE state with the EAR reading visible
   - Closing your eyes until the alarm triggers (red flash + SLEEPING label)
   - Opening your eyes and the alarm stopping
4. Export as GIF and save it as `demo.gif` in the repo root
5. Uncomment this line in the README:
```markdown
![Demo](demo.gif)
```

---

## Known Warnings (Safe to Ignore)

These messages appear on every run and are **not errors**:
```
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
W0000 ... Feedback manager requires a model with a single signature inference.
```
These are internal MediaPipe/TFLite diagnostics and do not affect functionality.

---

## Acknowledgements

- [MediaPipe](https://google.github.io/mediapipe/) by Google — Face Mesh landmark detection
- [OpenCV](https://opencv.org/) — Webcam capture and frame rendering
- [Pygame](https://www.pygame.org/) — Audio playback
- EAR formula based on the original paper by Soukupová & Čech (2016)
