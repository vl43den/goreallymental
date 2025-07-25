# Gesture Launcher Installation and Usage Guide

## 1. Installation Steps

### Install Python and pip (if not already installed)
```bash
sudo pacman -S python python-pip
```

### Install required Python packages

**IMPORTANT**: MediaPipe doesn't support Python 3.13+ yet. Arch only has Python 3.13 in official repos. Here are working solutions:

**Method 1: Use pyenv to install Python 3.11 (RECOMMENDED)**
```bash
# Install pyenv
sudo pacman -S pyenv

# Install Python 3.11 via pyenv
pyenv install 3.11.9
pyenv local 3.11.9

# Create virtual environment
python -m venv venv_py311
source venv_py311/bin/activate
pip install opencv-python mediapipe

# Test the installation
python -c "import cv2; import mediapipe; print('Success!')"
```

**Method 2: Use AUR packages**
```bash
# Install yay if you don't have it
sudo pacman -S --needed base-devel git
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si

# Try AUR Python versions
yay -S python311
# Then create venv with: python3.11 -m venv venv_py311
```

**Method 3: Use conda/miniconda (EASIEST)**
```bash
# Install miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# Restart terminal or source ~/.bashrc

# Create environment with Python 3.11
conda create -n gesture_env python=3.11
conda activate gesture_env

# Install opencv via conda, mediapipe via pip
conda install -c conda-forge opencv
pip install mediapipe

# Test
python -c "import cv2; import mediapipe; print('Success!')"
```

**Method 4: Use Docker (alternative)**
```bash
# Create Dockerfile with Python 3.11
sudo pacman -S docker
# Then use python:3.11 base image
```

Note: pyautogui is not needed for this implementation as we use subprocess for launching applications.

### Make the script executable (optional)
```bash
chmod +x gesture_launcher.py
```

## 2. Configuration

The `gestures.json` file maps finger counts to shell commands. You can edit this file to customize which applications launch for each gesture:

- **0 fingers (fist)**: gnome-terminal
- **1 finger**: nautilus (file manager)
- **2 fingers (peace sign)**: firefox
- **3 fingers**: code (VS Code)
- **4 fingers**: gedit
- **5 fingers (open palm)**: thunderbird

## 3. Running the Application

**If using pyenv + virtual environment (Method 1):**
```bash
source venv_py311/bin/activate
python gesture_launcher.py
```

**If using conda (Method 3):**
```bash
conda activate gesture_env
python gesture_launcher.py
```

**If using AUR python311 (Method 2):**
```bash
source venv_py311/bin/activate
python gesture_launcher.py
```

**If using Docker (Method 4):**
```bash
docker run -it --device=/dev/video0 -v $(pwd):/app python:3.11 bash
# Then inside container: cd /app && pip install opencv-python mediapipe && python gesture_launcher.py
```

## 4. Usage Instructions

1. Position your hand in front of the webcam
2. Hold up the desired number of fingers
3. The application will detect the gesture and launch the corresponding program
4. A 5-second cooldown prevents rapid re-launching
5. Press **ESC** to exit the application

## 5. Troubleshooting

- Ensure your webcam is working and not used by another application
- Check that the applications in `gestures.json` are installed on your system
- Adjust lighting for better hand detection
- Keep your hand steady and well-lit for accurate finger counting

## 6. Customization

Edit `gestures.json` to map different finger counts to your preferred applications:

```json
{
    "0": "your-command-here",
    "2": "firefox --new-window",
    "5": "nautilus ~/Documents"
}
```

You can use any shell command, including commands with arguments.
