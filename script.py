import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from playsound import playsound
import threading

# Path to your alert sound
ALERT_SOUND = 'alert.mp3'

# Function to play alert sound without blocking camera
def play_alert():
    threading.Thread(target=playsound, args=(ALERT_SOUND,), daemon=True).start()

# Open camera
cap = cv2.VideoCapture(0)  # Use 0 for default webcam

print("Study Tracker started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect objects
    bbox, labels, conf = cv.detect_common_objects(frame)

    # If phone detected, play alert
    if 'cell phone' in labels:
        print("Phone detected! Stay focused!")
        play_alert()

    # Draw bounding boxes and labels
    out = draw_bbox(frame, bbox, labels, conf)

    # Show the video feed
    cv2.imshow("Study Tracker - Press 'q' to quit", out)

    # Quit if 'q' pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()