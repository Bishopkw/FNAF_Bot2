# FNAF 1 4/20 Mode Automation Bot

## Project Overview

This project is a bot designed to automate gameplay in "Five Nights at Freddy's" (FNAF) 1, specifically for the 4/20 mode challenge. The bot uses Python and libraries like `pyautogui`, `pygetwindow`, and `tensorflow` to interact with the game screen, automate mouse movements, and perform actions based on pixel recognition.

See it in action [here](https://youtu.be/wX2QkcvJXC0).

## Features

- Automatically checks camera feeds and animatronic positions
- Moves the mouse and clicks on lights and doors as needed
- Reads pixel data to determine the presence of enemies like Freddy, Foxy, Bonnie, and Chica
- Optimized for the 4/20 difficulty mode

## Requirements

- Python 3.x
- `pyautogui` library for automating mouse movements
- `pygetwindow` library for interacting with the game window
- FNAF 1 installed and running in windowed mode

## Installation

1. **Install Python**: If you don’t have Python installed, download it from [here](https://www.python.org/downloads/).

2. **Install dependencies**:
   - Open a terminal or command prompt.
   - Install the necessary libraries by running:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set up FNAF 1**:
   - Run FNAF 1 in windowed mode so the bot can interact with the game window.
   - Ensure that the game window's title matches the one specified in the script (you can customize this if needed).

## How It Works

1. The bot identifies the game window using `pygetwindow`.
2. It uses `pyautogui` to move the mouse to specific screen locations (such as lights, doors, and the camera button) and performs clicks.
3. It checks pixel values at certain screen coordinates to determine the presence of animatronics and makes decisions based on that data.
4. Uses Tensorflow to check camera 4B and determine if Freddy, Chica or nobody is there.
5. The bot loops through these actions to survive the night in 4/20 mode.
- Check for Bonnie
- Check camera 4B
- Check for Chica only if she was seen on the camera.

## Getting Started

1. Clone this repository or download the code files.
2. Minimize FNAF by entering:
    ```bash
    alt + enter
3. Run the bot script by executing the following command:
   ```bash
   python main.py
4. Move the mouse to the top left corner of your monitor to exit. You might have to try a few times.
