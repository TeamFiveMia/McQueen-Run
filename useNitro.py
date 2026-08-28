import time

PEACE_CLASS = 1
CONF_THRESHOLD = 0.7

nitro = 0
vulnerable = True     
boost = False
boost_time = 2
endTime = 0


def nitro_add():
    global nitro
    nitro += 1
def after_detection():
    global nitro, vulnerable, boost, endTime
    if nitro > 0 and not boost:
        nitro -= 1
        vulnerable = False
        boost = True
        endTime = time.time() + boost_time
def response():
    global vulnerable, boost
    if boost and time.time() >= endTime:
        boost = False
        vulnerable = True
        return "Nitro Done", True
    return "Nitro not Done", False


def get_peace(result):
    priority = None
    highest_conf = 0.0

    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        if class_id == PEACE_CLASS and confidence > CONF_THRESHOLD:
            if confidence > highest_conf:
                highest_conf = confidence
                x1, y1, x2, y2 = tuple(box.xyxy[0])
                priority = (x1, y1, x2, y2)

    return priority