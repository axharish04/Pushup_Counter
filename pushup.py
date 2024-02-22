import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
import threading

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

people = {}  # Dictionary to store people and their pushup counts
curr_per = None
curr_cnt = 0
curr_pos = "UP"

# GUI for person's name input
def start_pushup():
    global curr_per
    curr_per = name_entry.get()
    if curr_per not in people:
        people[curr_per] = 0
    start_pushup_button['state'] = 'disabled'
    threading.Thread(target=process_pushups).start()

root = tk.Tk()
root.title("Push-up Count Leaderboard")

name_label = tk.Label(root, text="Enter Your Name:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()
start_pushup_button = tk.Button(root, text="Start Pushup", command=start_pushup)
start_pushup_button.pack()

lead_label = tk.Label(root, text="Leaderboard:")
lead_label.pack()
txt = tk.Text(root, height=10, width=40)
txt.pack()

# Function to update the leaderboard
def update_leaderboard():
    sorted_people = dict(sorted(people.items(), key=lambda item: item[1], reverse=True))
    txt.delete(1.0, tk.END)
    rank = 1
    for person, pushups in sorted_people.items():
        txt.insert(tk.END, f"{rank}. {person}: {pushups} pushups\n")
        rank += 1
    txt.after(1000, update_leaderboard)

update_leaderboard()
#txt.tag_configure("leaderboard", font=("Arial", 12), foreground="white", background="blue")
def process_pushups():
    global curr_cnt, curr_pos
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                angle = (calculate_angle(left_shoulder, left_elbow, left_wrist) +
                         calculate_angle(right_shoulder, right_elbow, right_wrist)) / 2

                if curr_pos == "UP" and angle < 90:
                    curr_pos = "DOWN"
                elif curr_pos == "DOWN" and angle > 160:
                    curr_pos = "UP"
                    if curr_per is not None:
                        people[curr_per] += 1
                        curr_cnt = people[curr_per]

            except:
                pass


            cv2.rectangle(image, (0, 0), (200, 75), (255, 0, 0), -1)
            cv2.putText(image, 'REPS', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, str(curr_cnt), (85, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 6, cv2.LINE_AA)

            cv2.rectangle(image, (220, 0), (450, 75), (255, 0, 0), -1)
            cv2.putText(image, 'STAGE', (230, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, curr_pos, (280, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 114, 67), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 69, 222), thickness=2, circle_radius=2))

            cv2.imshow('Pushup Counter', image)

            if cv2.waitKey(10) & 0xFF == ord('z'):
                break

        cap.release()
        cv2.destroyAllWindows()
        start_pushup_button['state'] = 'normal'

root.mainloop()
