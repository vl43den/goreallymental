# 🤚 Gesture Launcher

**Control your computer with hand gestures!** A Python application that uses computer vision to detect hand gestures and launch applications via webcam.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10+-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)

## ✨ Features

- 🎯 **Real-time hand detection** using Google's MediaPipe
- 👆 **Finger counting** (0-5 fingers) for gesture recognition
- 🚀 **Customizable app launching** via JSON configuration
- ⏱️ **5-second cooldown** to prevent accidental launches
- 📹 **Visual feedback** with hand landmarks overlay
- 🎨 **Clean interface** showing gesture status and available commands
- ⚙️ **Easy configuration** - edit gestures without touching code

## 🎮 Default Gestures

| Gesture | Fingers | Action |
|---------|---------|--------|
| ✊ Fist | 0 | Open Terminal |
| ☝️ Point | 1 | Open File Manager |
| ✌️ Peace | 2 | Open Firefox → YouTube |
| 🤟 Three | 3 | Open VS Code |
| 🖖 Four | 4 | Open Text Editor |
| ✋ Open Hand | 5 | Open Thunderbird |

## 🚀 Quick Start

### Prerequisites
- **Arch Linux** (or similar)
- **Python 3.11+**
- **Webcam**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vl43den/goreallymental.git
   cd goreallymental
   ```

2. **Set up Python environment** (choose one method):

   **Option A: Using Conda (Recommended)**
   ```bash
   # Install miniconda
   curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   
   # Create environment
   conda create -n gesture_env python=3.11
   conda activate gesture_env
   conda install -c conda-forge opencv
   pip install mediapipe
   ```

   **Option B: Using pyenv**
   ```bash
   sudo pacman -S pyenv
   pyenv install 3.11.9
   pyenv local 3.11.9
   python -m venv venv_py311
   source venv_py311/bin/activate
   pip install opencv-python mediapipe
   ```

3. **Run the application**
   ```bash
   conda activate gesture_env  # or source venv_py311/bin/activate
   python gesture_launcher.py
   ```

4. **Start gesturing!** ✋
   - Position your hand in front of the webcam
   - Hold up fingers (0-5) to trigger actions
   - Press **ESC** to exit

## ⚙️ Customization

Edit `gestures.json` to customize your gesture mappings:

```json
{
    "0": "gnome-terminal",
    "1": "nautilus ~/Documents",
    "2": "firefox https://github.com",
    "3": "code .",
    "4": "gedit",
    "5": "spotify"
}
```

You can use any shell command, including:
- Commands with arguments: `"firefox --private-window"`
- File paths: `"nautilus ~/Downloads"`
- Scripts: `"/path/to/your/script.sh"`

## 🛠️ How It Works

1. **Camera Capture**: OpenCV captures video from your webcam
2. **Hand Detection**: MediaPipe identifies hand landmarks (21 points)
3. **Finger Counting**: Algorithm analyzes fingertip positions relative to joints
4. **Gesture Mapping**: Finger count is matched to commands in `gestures.json`
5. **Cooldown Check**: 5-second timer prevents rapid re-execution
6. **Command Execution**: Shell command runs in background via subprocess

## 📁 Project Structure

```
goreallymental/
├── gesture_launcher.py    # Main application
├── gestures.json         # Gesture configuration
├── INSTALLATION.md       # Detailed setup guide
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## 🔧 Technical Details

- **Hand Detection**: MediaPipe Hands solution with 21 landmark points
- **Finger Detection**: Compares fingertip Y-coordinates with joint positions
- **Thumb Special Case**: Uses X-coordinate comparison for thumb detection
- **Performance**: 30+ FPS processing with minimal CPU usage
- **Cooldown**: `time.monotonic()` for precise timing

## 🐛 Troubleshooting

### Camera Issues
- Ensure webcam is not used by another application
- Check camera permissions: `ls /dev/video*`
- Try different camera index if needed

### Import Errors
- Verify Python version: `python --version` (should be 3.11+)
- Check MediaPipe compatibility with your Python version
- Ensure you're in the correct virtual environment

### Poor Detection
- Improve lighting conditions
- Keep hand steady and well-positioned
- Ensure contrasting background
- Clean your camera lens

### App Launch Issues
- Verify applications are installed: `which firefox`
- Check command syntax in `gestures.json`
- Test commands manually in terminal first

## 🔮 Future Enhancements

- [ ] Multi-hand gesture combinations
- [ ] Custom gesture recording
- [ ] Profile system (work/gaming/dev modes)
- [ ] Voice command integration
- [ ] System tray integration
- [ ] GUI configuration editor
- [ ] Gesture sequence support
- [ ] Mobile companion app

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google MediaPipe** - For excellent hand tracking technology
- **OpenCV** - For computer vision capabilities
- **Python Community** - For amazing libraries and support

## 📧 Contact

- **Author**: vl43den
- **Email**: is231338@fhstp.ac.at
- **GitHub**: [@vl43den](https://github.com/vl43den)

---

**⭐ If this project helped you, please give it a star!**

Made with ❤️ and Python 🐍goreallymental
Let‘s do it with GO
