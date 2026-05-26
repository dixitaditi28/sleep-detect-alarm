import cv2
import numpy as np
import mediapipe as mp #Called Aliasing by using the as keyword. we give the libraries a nickname. np and mp are universally used for numpy and mediapipe respectively
import time
import os
import threading 


# We use try-except block as a safety net to check if the pygame library is available for playing alarm sounds. If it's not installed, we can handle that gracefully without crashing the program.
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("[WARNING] pygame library not found. Install it with: pip install pygame")

# ---CONFIGURATION SETTINGS---
# EAR stands for Eye Aspect Ratio, a simple mathematical formula used in Computer Vision
# to determine if a person's eyes are open or closed based on the positions of specific facial landmarks around the eyes. 
# the r indicates a raw string literal, which tells Python to treat backslashes as literal characters and not as escape characters.
#  This is particularly useful when dealing with file paths on Windows, where backslashes are commonly used. By using a raw string, we can avoid issues with escape sequences 
# and ensure that the file path is interpreted correctly.

EAR_THRESHOLD = 0.22
EYE_CLOSED_SECONDS = 2.5
# In our previous snippet, we set ALARM_SOUND_PATH = r"C:\Users\dixit\Desktop\...". 
# Because os.path.join is smart, if it sees that the second part is already an absolute path (starting with C:\), 
# it just ignores the first part.
# the dynamic pathing we just wrote in play_alarm() will work perfectly 
# Python will find it automatically! This means if we ever move this folder to a new computer or a different drive, the code won't break.

ALARM_SOUND_PATH = r"drama-queen-alarm.mp3" 

LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]


def eye_aspect_ratio(landmarks, eye_indices, frame_w, frame_h):
    pts = []
    for idx in eye_indices:
        lm = landmarks[idx]
        pts.append(np.array([lm.x * frame_w, lm.y * frame_h]))
    A = np.linalg.norm(pts[1] - pts[5]) # Vertical distance between points 2 and 6
    B = np.linalg.norm(pts[2] - pts[4]) # Vertical distance between points 3 and 5
    C = np.linalg.norm(pts[0] - pts[3]) # Horizontal distance between points 1 and 4
    ear = (A + B) / (2.0 * C)
    return ear

def play_alarm():
    if not PYGAME_AVAILABLE:
        print("\a[ALARM] Eyes closed for too long! (No sound - pygame not available)")
        return
    sound_path = os.path.join(os.path.dirname(__file__), ALARM_SOUND_PATH)
    if not os.path.isfile(sound_path):
        print(f"[ALARM] sound file not found: {sound_path}")
        print("\a")    
        return
    try:
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1) # Loop indefinitely
    except Exception as e:
        print(f"[ERROR] Failed to play alarm sound: {e}")
        print("\a") # Fallback to system beep    