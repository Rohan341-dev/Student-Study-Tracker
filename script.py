import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

# Open default webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect common objects in the frame
    bbox, labels, conf = cv.detect_common_objects(frame)

    # Draw bounding boxes on the frame
    out = draw_bbox(frame, bbox, labels, conf)

    # Print detected objects in console
    if labels:
        print("Objects detected:", labels)

    # Show video with bounding boxes
    cv2.imshow("Object Detection", out)

    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()