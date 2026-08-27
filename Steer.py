# Palm gesture Steering 

PALM_CLASS = 0
CONF_THRESHOLD = 0.6

# Get the Car position in Pixels
def calc_position(lane, lane_width):

    # Calculate the Car Position (neglect decimals)
    position = int(lane_width * lane + lane_width / 2)

    return position


def get_lane(x_center, lane_width, no_lanes):

    # Return the index of the lane
    lane = int((x_center / lane_width) + 1)
    # Ensure that lane is not greater than last valid lane
    lane = min(lane, no_lanes)

    return lane  

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
