import cv2 as cv
import numpy as np



def main():

    # Get the Coordinates from YOLO detection

    # Game settings
    frame_width = 640
    frame_height = 480
    lanes = 5

    # Calculate Lane Width
    Lane_width = frame_width / lanes

    while True:
        palm_box = get_palm(result)

        if palm_box is not None:


            # Create game screen (rows x columns)
            frame = np.zeros((frame_height, frame_width, 3), dtype = np.uint8)

            # Calculate the x coordinate for the center of the box
            x_center = (x1 + x2) / 2

            # Get the lane index
            lane = get_lane(x_center, Lane_width, lanes)

            # Calculate the car position
            car_position = calc_position(lane, Lane_width)


         
         


# Get the Car position in Pixels
def calc_position(lane, lane_width):

    # Calculate the Car Position (neglect decimals)
    position = int(lane_width * lane + lane_width / 2)

    return position


def get_lane(x_center, lane_width, no_lanes):

    # Return the index of the lane
    lane = int((x_center / lane_width))
    # Ensure that lane is not greater than last valid lane
    lane = min(lane, no_lanes - 1)

    return lane  

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


if __name__ == "__main__":
    main()