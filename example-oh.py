"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import math
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

class Center:
    def __init__(self):
        self.temp_axis = []
        self.temp_mean_x = 0
        self.temp_mean_y = 0
        self.max_length = 6

    def centerized(self, x, y):
        self.temp_axis.append((x, y))
    
        if len(self.temp_axis) < self.max_length:
            pass
        else:
            temp_total_x = 0
            temp_total_y = 0
            for i in range(self.max_length):
                for j in range(2):
                    if j == 0:
                        temp_total_x += self.temp_axis[i][j]
                    elif j == 1:
                        temp_total_y += self.temp_axis[i][j]
                    else:
                        pass
            del self.temp_axis[0]
            self.temp_mean_x = temp_total_x // self.max_length
            self.temp_mean_y = temp_total_y // self.max_length
        return (self.temp_mean_x, self.temp_mean_y)

c = Center()

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    horizontal_ratio = gaze.horizontal_ratio()
    vertical_ratio = gaze.vertical_ratio()

    mimicked_x = 0
    mimicked_y = 0

    if horizontal_ratio is not None and vertical_ratio is not None:
        mimicked_x = math.floor(640 * horizontal_ratio) - 30
        mimicked_y = math.floor(480 * vertical_ratio) + 20
        centerized_axis = c.centerized(mimicked_x, mimicked_y)
    else:
        pass

    cv2.putText(frame, "L pupil: " + str(left_pupil), (0, 130), cv2.FONT_HERSHEY_DUPLEX, 0.6, (147, 58, 31), 1)
    cv2.putText(frame, "R pupil: " + str(right_pupil), (0, 165), cv2.FONT_HERSHEY_DUPLEX, 0.6, (147, 58, 31), 1)

    cv2.putText(frame, "Hor    : " + str(horizontal_ratio), (0, 200), cv2.FONT_HERSHEY_DUPLEX, 0.6, (147, 58, 31), 1)
    cv2.putText(frame, "Ver    : " + str(vertical_ratio), (0, 235), cv2.FONT_HERSHEY_DUPLEX, 0.6, (147, 58, 31), 1)

    cv2.putText(frame, "+", centerized_axis, cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 3)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
