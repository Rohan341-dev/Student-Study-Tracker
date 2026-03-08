import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    # Filter results for only "cell phone"
    detections = results[0].boxes
    labels = results[0].names

    for box in detections:
        cls_id = int(box.cls[0])
        class_name = labels[cls_id]

        if class_name == "cell phone":
            xyxy = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = xyxy.astype(int)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.9, (0, 0, 255), 2)

            print("🚨 Phone detected!")

    cv2.imshow("Phone Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()