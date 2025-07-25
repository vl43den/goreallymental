#!/usr/bin/env python3
"""
Gesture Launcher - Launch applications using hand gestures
Author: Python Expert Assistant
Description: Uses OpenCV and MediaPipe to detect hand gestures and launch applications
"""

import cv2
import mediapipe as mp
import json
import subprocess
import time
import sys
import os

class GestureLauncher:
    def __init__(self, config_file='gestures.json'):
        """Initialize the gesture launcher with MediaPipe and OpenCV"""
        # Initialize MediaPipe hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,  # Only detect one hand
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam")
        
        # Load gesture configuration
        self.config_file = config_file
        self.gesture_commands = self.load_gestures()
        
        # Cooldown management
        self.last_gesture_time = 0
        self.cooldown_duration = 10.0  # 5 seconds cooldown
        
        print("Gesture Launcher initialized!")
        print("Available gestures:", list(self.gesture_commands.keys()))
        print("Press ESC to exit\n")
    
    def load_gestures(self):
        """Load gesture-to-command mappings from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                gestures = json.load(f)
            print(f"Loaded gestures from {self.config_file}")
            return gestures
        except FileNotFoundError:
            print(f"Warning: {self.config_file} not found. Using default gestures.")
            # Default gestures if file doesn't exist
            return {
                "0": "gnome-terminal",
                "1": "nautilus",
                "2": "firefox",
                "3": "code",
                "4": "gedit",
                "5": "thunderbird"
            }
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.config_file}. Using default gestures.")
            return {"0": "gnome-terminal", "2": "firefox", "5": "thunderbird"}
    
    def count_fingers(self, landmarks):
        """
        Count the number of fingers held up based on hand landmarks
        Returns: integer count of fingers (0-5)
        """
        # Finger tip and pip (proximal interphalangeal) landmark indices
        # Thumb: tip=4, pip=3
        # Index: tip=8, pip=6
        # Middle: tip=12, pip=10
        # Ring: tip=16, pip=14
        # Pinky: tip=20, pip=18
        
        finger_tips = [4, 8, 12, 16, 20]
        finger_pips = [3, 6, 10, 14, 18]
        
        fingers_up = 0
        
        # Check thumb (special case - compare x coordinates)
        if landmarks[finger_tips[0]].x > landmarks[finger_pips[0]].x:
            fingers_up += 1
        
        # Check other four fingers (compare y coordinates)
        for i in range(1, 5):
            if landmarks[finger_tips[i]].y < landmarks[finger_pips[i]].y:
                fingers_up += 1
        
        return fingers_up
    
    def launch_command(self, command):
        """Launch a shell command in the background"""
        try:
            subprocess.Popen(command, shell=True, 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            print(f"✓ Launched: {command}")
        except Exception as e:
            print(f"✗ Failed to launch {command}: {e}")
    
    def is_cooldown_active(self):
        """Check if we're still in cooldown period"""
        return time.monotonic() - self.last_gesture_time < self.cooldown_duration
    
    def process_gesture(self, finger_count):
        """Process detected gesture and launch corresponding command"""
        finger_str = str(finger_count)
        
        # Check if gesture is mapped and cooldown is over
        if finger_str in self.gesture_commands and not self.is_cooldown_active():
            command = self.gesture_commands[finger_str]
            print(f"Detected {finger_count} fingers → launching {command}")
            self.launch_command(command)
            self.last_gesture_time = time.monotonic()
    
    def draw_info(self, image, finger_count, landmarks):
        """Draw hand landmarks and finger count on the image"""
        height, width, _ = image.shape
        
        # Draw hand landmarks
        self.mp_drawing.draw_landmarks(
            image, landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        # Draw finger count
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        color = (0, 255, 0)  # Green
        thickness = 3
        
        text = f"Fingers: {finger_count}"
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (width - text_size[0]) // 2
        text_y = 50
        
        cv2.putText(image, text, (text_x, text_y), font, font_scale, color, thickness)
        
        # Draw cooldown indicator
        if self.is_cooldown_active():
            remaining = self.cooldown_duration - (time.monotonic() - self.last_gesture_time)
            cooldown_text = f"Cooldown: {remaining:.1f}s"
            cv2.putText(image, cooldown_text, (10, height - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Draw available gestures
        y_offset = 100
        for gesture, command in self.gesture_commands.items():
            gesture_text = f"{gesture}: {command}"
            cv2.putText(image, gesture_text, (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 25
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                # Read frame from camera
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to read from camera")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process frame with MediaPipe
                results = self.hands.process(rgb_frame)
                
                finger_count = 0
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Count fingers
                        finger_count = self.count_fingers(hand_landmarks.landmark)
                        
                        # Process gesture
                        self.process_gesture(finger_count)
                        
                        # Draw landmarks and info
                        self.draw_info(frame, finger_count, hand_landmarks)
                        break  # Only process first hand
                else:
                    # No hand detected
                    cv2.putText(frame, "No hand detected", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Show frame
                cv2.imshow('Gesture Launcher', frame)
                
                # Check for ESC key press
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC key
                    print("\nExiting gesture launcher...")
                    break
                    
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Cleanup
            self.cap.release()
            cv2.destroyAllWindows()
            print("Cleanup complete")

def main():
    """Main function"""
    try:
        launcher = GestureLauncher()
        launcher.run()
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
