# Palm Steering
PALM_CLASS = 0
CONF_THRESHOLD = 0.6


def get_palm(result):
    priority = None
    highest_conf = 0.0

    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        if class_id == PALM_CLASS and confidence > CONF_THRESHOLD:
            if confidence > highest_conf:
                highest_conf = confidence
                x1, y1, x2, y2 = tuple(box.xyxy[0])
                priority = (x1, y1, x2, y2)

    return priority