class FakeBox:

    def __init__(self, class_id, confidence, coordinates):
        self.cls = [class_id]
        self.conf = [confidence]
        self.xyxy = [coordinates]


class FakeResult:

    def __init__(self, boxes):
        self.boxes = boxes


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


# Pretend YOLO detected two things
box1 = FakeBox(
    class_id=0,
    confidence=0.60,
    coordinates=[50, 100, 150, 250]
)

box2 = FakeBox(
    class_id=0,
    confidence=0.94,
    coordinates=[300, 100, 400, 250]
)

box3 = FakeBox(
    class_id=0,
    confidence=0.75,
    coordinates=[500, 100, 600, 250]
)

result = FakeResult([box1, box2, box3])


palm_box = get_palm(result)


print("Palm box:", palm_box)