"""
Student Study Tracker
---------------------
- Monitors the student via webcam.
- Detects cell phones using YOLOv8 (COCO class 67).
- Draws bounding boxes around detected phones.
- Plays an alert sound (alert.mp3) when a phone first appears.
- Logs total distraction time in seconds.
- Press 'q' to quit.
"""

import cv2
from ultralytics import YOLO
import threading
import time
from playsound import playsound
import sys


print("Loading YOLOv8 model...")
model = YOLO('yolov8n.pt')  
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit(1)

# ------------------------------------------------------------
# 3. Initialize variables for distraction tracking and timing
# ------------------------------------------------------------
total_distraction_time = 0.0      # accumulated seconds of phone distraction
phone_detected_prev = False        # was a phone detected in the previous frame?
last_frame_time = time.time()      # used to compute time between frames

# For optional FPS display (helps verify performance)
frame_count = 0
fps = 0
last_fps_time = time.time()
fps_display_interval = 1.0         # update FPS every second

# ------------------------------------------------------------
# 4. Function to play the alert sound in a separate thread
#    (so it doesn't block the main detection loop)
# ------------------------------------------------------------
def play_alert():
    try:
        playsound('')      # make sure alert.mp3 is in the same folder
    except Exception as e:
        print(f"Could not play sound: {e}")

print("\nTracker started. Press 'q' to quit.\n")

# ------------------------------------------------------------
# 5. Main loop: capture frames, run detection, update logs, show output
# ------------------------------------------------------------
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Calculate time elapsed since last frame (for distraction time)
    current_time = time.time()
    delta_time = current_time - last_frame_time
    last_frame_time = current_time

    # --------------------------------------------------------
    # Run YOLO detection on the current frame
    # --------------------------------------------------------
    results = model(frame)          # results is a list, we use the first (and only) image

    phone_detected_current = False   # flag for this frame

    # Check all detected objects
    if results[0].boxes is not None:
        for box in results[0].boxes:
            class_id = int(box.cls[0])          # class ID (COCO: 67 = cell phone)
            if class_id == 67:                   # we only care about cell phones
                phone_detected_current = True

                # Get bounding box coordinates and confidence
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]

                # Draw the bounding box and label on the frame
                label = f"Phone {confidence:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # --------------------------------------------------------
    # Update total distraction time (add time for every frame where phone is present)
    # --------------------------------------------------------
    if phone_detected_current:
        total_distraction_time += delta_time

    # --------------------------------------------------------
    # Play alert sound ONLY when a phone first appears (not every frame)
    # --------------------------------------------------------
    if phone_detected_current and not phone_detected_prev:
        threading.Thread(target=play_alert, daemon=True).start()

    # Remember current detection state for the next frame
    phone_detected_prev = phone_detected_current

    # --------------------------------------------------------
    # (Optional) Calculate and display FPS for performance monitoring
    # --------------------------------------------------------
    frame_count += 1
    if current_time - last_fps_time >= fps_display_interval:
        fps = frame_count / (current_time - last_fps_time)
        frame_count = 0
        last_fps_time = current_time

    # --------------------------------------------------------
    # Overlay distraction time and FPS on the video feed
    # --------------------------------------------------------
    cv2.putText(frame, f"Total Distraction: {total_distraction_time:.1f} sec",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # --------------------------------------------------------
    # Show the live feed with detections
    # --------------------------------------------------------
    cv2.imshow('Student Study Tracker', frame)

    # --------------------------------------------------------
    # Exit when 'q' is pressed
    # --------------------------------------------------------
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ------------------------------------------------------------
# 6. Cleanup: release camera and close windows
# ------------------------------------------------------------
cap.release()
cv2.destroyAllWindows()
print(f"\nSession ended. Total distraction time: {total_distraction_time:.2f} seconds")