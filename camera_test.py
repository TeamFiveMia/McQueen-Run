# Testing the Camera
import cv2 as cv
from ultralytics import YOLO

def get_palm(result):

    priority = None
    highest_conf = 0.0

    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        if class_id == 0 and confidence > 0.5:

            if confidence > highest_conf:
                highest_conf = confidence

            x1, y1, x2, y2 = tuple(box.xyxy[0])

            priority = (x1, y1, x2, y2)

    return priority

model = YOLO("yolo11n.pt")


camera = cv.VideoCapture(0)

while True:

    success, frame = camera.read()

    if not success:
        break

    results = model(frame)

    box = results[0].boxes

    class_id = int(box.cls[0])
    confidence = float(box.conf[0])
    x1, y1, x2, y2 = tuple(box.xyxy[0])

    print(class_id, confidence, x1, y1, x2, y2)

    detected_frame = results[0].plot()

    cv.imshow("Camera Test", detected_frame)

    key = cv.waitKey(1)

    if key == 27:
        break

camera.release()
cv.destroyAllWindows()