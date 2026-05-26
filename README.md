# Sleep Alarm Detector 💤🚨

A Python-based computer vision project that monitors your webcam feed to detect if you fall asleep at your desk. It calculates the Eye Aspect Ratio (EAR) using AI facial landmarks and triggers an audio alarm to wake you up if your eyes stay closed for too long.

## Features (In Progress)
* **Face & Eye Tracking:** Uses Google's MediaPipe Face Mesh to accurately track 3D facial landmarks and calculate the EAR.
* **Smart Audio Fallbacks:** Uses Pygame for smooth, threaded audio playback, with a built-in safety net that triggers the motherboard system beep if the audio file or library is missing.
* **Dynamic Configuration:** Easily adjustable thresholds for eye-closure sensitivity and alarm delay time.

## Requirements
* Python 3.8+
* A working webcam

## Installation & Setup

1. **Install the dependencies:**
   ```bash
   pip install mediapipe opencv-python numpy pygame-ce