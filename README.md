## Overview
Interactive Pool is an innovative video processing application designed specifically for tracking cue sticks and billiard balls in real-time. Utilizing advanced image processing techniques with OpenCV, the program not only tracks these objects but also predicts the trajectories of the billiard balls, enhancing the experience of playing or viewing a game of pool.

## Key Features
- **Real-time Cue Stick and Ball Tracking:** Uses camera feed to accurately track the movement of the cue stick and billiard balls on a pool table.
- **Trajectory Prediction:** Predicts the paths of billiard balls after being hit, aiding in strategic gameplay and shot planning.
- **Circle and Line Detection:** Employs Hough Circle Transform for ball detection and Hough Line Transform for cue stick detection, refined with edge detection techniques.
- **Visual Enhancements:** Offers visual overlays on the video feed, showing predicted paths and impact points, enhancing the interactive experience.

## System Requirements
- **Camera:** A webcam or an external camera capable of capturing clear video of the pool table.
- **Python Environment:** Python 3.x with OpenCV library installed.
- **Additional Libraries:** NumPy for numerical operations and mathematical calculations.

## Installation and Setup
1. **Install Python:** Ensure Python 3.x is installed on your system.
2. **Install Dependencies:** Use pip to install required libraries:
   ```
   pip install opencv-python numpy
   ```
3. **Connect Camera:** Set up your camera to have a clear, unobstructed view of the pool table.
4. **Run the Program:** Execute the script to start tracking and enjoy an enhanced pool playing experience.

## Usage
- Position the camera to cover the entire pool table.
- Run the Interactive Pool application.
- The program will automatically start detecting the cue stick and balls, displaying their trajectories on the screen.

## Limitations
- The accuracy of tracking and trajectory prediction depends on the quality of the camera and lighting conditions.
- Currently supports a single pool table setup.