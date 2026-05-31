# Troubleshooting: MediaPipe `AttributeError: module 'mediapipe' has no attribute 'solutions'` on Windows

> **Project:** Sleep Detect Alarm  
> **OS:** Windows 11  
> **Environment:** Anaconda (base), Python 3.11.5  
> **IDE:** VS Code with PowerShell terminal

---

## The Full Problem Chain

This error is almost never just one issue. It is a chain of 5 compounding problems that must be fixed in order:

1. Wrong Python version (3.14 is unsupported by MediaPipe)
2. NumPy 2.0 binary incompatibility with MediaPipe's C++ layer
3. OpenCV version conflict with NumPy 1.x
4. PowerShell execution policy blocking Anaconda's activation script
5. VS Code using the wrong Python interpreter
6. Webcam index mismatch (`cv2.VideoCapture(1)` instead of `0`)

---

## Final Working Environment

| Package | Version |
|---|---|
| Python | 3.11.5 (Anaconda base) |
| mediapipe | 0.10.14 |
| numpy | 1.26.4 |
| opencv-python | 4.10.0.84 |
| matplotlib | 3.8.4 |
| pygame | 2.5.7 |

---

## Step-by-Step Fix

### Problem 1 — Wrong Python Version

**Symptom:** MediaPipe install fails or `solutions` attribute is missing entirely.

**Cause:** MediaPipe does not support Python 3.12+ as of 2024-2025. Python 3.14 is completely unsupported.

**Fix:** Switch to Python 3.11 via Anaconda:
```powershell
# Verify you are on the correct version
python --version
# Must show Python 3.11.x
```

If not, create a fresh conda environment:
```powershell
conda create -n mp_env python=3.11.9 -y
conda activate mp_env
```

---

### Problem 2 — NumPy 2.0 Binary Incompatibility

**Symptom:**
```
ImportError: numpy.core.multiarray failed to import
```

**Cause:** MediaPipe's C++ extensions were compiled against NumPy 1.x. NumPy 2.0 removed `numpy.core` entirely, breaking binary compatibility.

**Fix:** Downgrade NumPy:
```powershell
pip uninstall numpy -y
pip install numpy==1.26.4 --no-cache-dir
```

---

### Problem 3 — matplotlib / NumPy Version Mismatch

**Symptom:**
```
ImportError: numpy.core.multiarray failed to import
  File "...matplotlib\colors.py"
  File "...matplotlib\scale.py"
  File "...matplotlib\ticker.py"
```

**Cause:** MediaPipe's `drawing_styles` module imports matplotlib. If matplotlib was compiled against NumPy 2.x, it breaks when NumPy 1.x is installed.

**Fix:** Pin matplotlib to the last version built for NumPy 1.x:
```powershell
pip uninstall matplotlib -y
pip install matplotlib==3.8.4 --no-cache-dir
```

---

### Problem 4 — PowerShell Execution Policy Blocking Conda

**Symptom:**
```
conda-hook.ps1 cannot be loaded because running scripts is disabled on this system.
conda : The term 'conda' is not recognized...
```

**Cause:** Windows blocks PowerShell scripts by default. Anaconda uses a `.ps1` hook script to activate environments, which gets blocked.

**Fix (run PowerShell as Administrator):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Type `Y` when prompted. Then reinitialize conda for PowerShell:
```powershell
C:\Users\<YourUsername>\anaconda3\Scripts\conda.exe init powershell
```
Close and reopen the terminal. You should now see `(base)` in your prompt.

---

### Problem 5 — VS Code Using the Wrong Python Interpreter

**Symptom:** Script runs fine from the terminal but fails when using the VS Code Run button (triangle), or `Ctrl+Shift+P` → "Python: Select Interpreter" shows no results.

**Cause 1:** The `.vscode/settings.json` may be overriding the conda environment with a different Python manager.

**Fix for `settings.json`** — replace its contents with:
```json
{
    "python.defaultInterpreterPath": "C:\\Users\\<YourUsername>\\anaconda3\\python.exe",
    "python.terminal.activateEnvironment": true,
    "python-envs.defaultEnvManager": "ms-python.python:conda",
    "python-envs.defaultPackageManager": "ms-python.python:pip"
}
```

**Cause 2:** The Python extension for VS Code is not installed.

**Fix:** Press `Ctrl+Shift+X`, search for **Python** by Microsoft, and install it.

**After fixing:** Press `Ctrl+Shift+P` → **Python: Select Interpreter** → choose:
```
Python 3.11.5 ('base': conda)  C:\Users\<YourUsername>\anaconda3\python.exe
```

> **Tip:** When in doubt, always run from the terminal instead of the triangle button:
> ```powershell
> python sleep-alarm.py
> ```
> This guarantees the correct Python is used.

---

### Problem 6 — Webcam Not Opening

**Symptom:**
```
[ERROR]
```

**Cause:** `cv2.VideoCapture(1)` looks for a second camera (index 1). Most laptops only have one built-in webcam at index 0.

**Fix:** Change this line in your script:
```python
# Before
cap = cv2.VideoCapture(1)

# After
cap = cv2.VideoCapture(0)
```

**To find your correct camera index**, run:
```powershell
python -c "
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f'Camera found at index {i}')
        cap.release()
    else:
        print(f'No camera at index {i}')
"
```

---

## Full Clean Reinstall (if all else fails)

Run these commands in order in a PowerShell terminal with `(base)` active:

```powershell
pip uninstall mediapipe numpy matplotlib opencv-python -y
pip cache remove mediapipe
pip install numpy==1.26.4 --no-cache-dir
pip install mediapipe==0.10.14 --no-cache-dir
pip install opencv-python==4.10.0.84 --no-cache-dir
pip install matplotlib==3.8.4 --no-cache-dir
```

Then verify everything works:
```powershell
python -c "import mediapipe as mp; import cv2; import numpy; print('All good!', mp.__version__, cv2.__version__, numpy.__version__)"
```

Expected output:
```
All good! 0.10.14 4.10.0.84 1.26.4
```

---

## How to Stop the Program

Click on the webcam window to give it focus, then press **Q**.

---

## Warning Messages You Can Safely Ignore

These appear on every run and are not errors:
```
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
W0000 ... Feedback manager requires a model with a single signature inference.
```
These are internal MediaPipe/TFLite diagnostics and do not affect functionality.
