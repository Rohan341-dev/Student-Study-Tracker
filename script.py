import cv2
from ultralytics import YOLO
import time

MODEL_PATH = "yolov8n.pt"
DETECTION_CLASS = "cell phone"
DISTRACTION_LOG_FILE = "distraction_log.txt"

model = YOLO(MODEL_PATH)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    exit()

distraction_time = 0
phone_detected_prev = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    detections = results[0].boxes
    labels_dict = results[0].names

    phone_detected = False

    for box in detections:
        cls_id = int(box.cls[0])
        class_name = labels_dict[cls_id]

        if class_name == DETECTION_CLASS:
            phone_detected = True
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            x1, y1, x2, y2 = xyxy
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, class_name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    if phone_detected:
        if not phone_detected_prev:
            start_time = time.time()
        else:
            distraction_time += 1 / 30

    phone_detected_prev = phone_detected

    cv2.putText(frame, f"Distraction Time: {int(distraction_time)} sec",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    cv2.imshow("Student Study Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

with open(DISTRACTION_LOG_FILE, "w") as f:
    f.write(f"Total distraction time: {int(distraction_time)} seconds\n")

print(f"Total distraction time: {int(distraction_time)} seconds")