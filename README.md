##Python Implementation of Pushup Counter Games

Dependencies
- numpy
- opencv==4.8.1
- tkinter
- mediapipe pose estimation


# Push-up Counter using Mediapipe

This project is a push-up counter that utilizes the Mediapipe library for pose estimation. It allows users to count their push-ups using their webcam and displays the count in real-time along with a leaderboard.

## Requirements

To use this project, you need to have the following:

- **Python**: Make sure you have Python installed on your system. You can download it from the [official Python website](https://www.python.org/).

- **Dependencies**: Install the required Python dependencies using pip. You can install them using the following command:

    ```
    pip install opencv-python mediapipe numpy tkinter
    ```

- **Webcam**: Ensure that your system has a working webcam. The push-up counter uses the webcam to detect and count push-up movements.

## How to Use

1. Clone this repository to your local machine:

    ```
    git clone https://github.com/axharish04/Pushup_Counter.git
    ```

2. Navigate to the project directory:

    ```
    cd pushup-counter
    ```

3. Run the main Python script:

    ```
    python pushup.py
    ```

4. When prompted, enter your name in the provided input field and click the "Start Pushup" button to begin. Follow the instructions displayed on the screen to perform push-ups. The program will count your push-ups and display the count in real-time.

5. After completing push-ups, you will see your name on the leaderboard along with the number of push-ups you've completed.

## Additional Notes

- Ensure that you have sufficient lighting in the room when using the push-up counter. Poor lighting conditions may affect pose detection accuracy.

- Ensure you make sure the entire upper body is visible in the camera to ensure higher accurate detection
"""


