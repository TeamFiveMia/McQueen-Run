import cv2 as cv
import numpy as np



def main():

    # Get the Coordinates from YOLO detection

    # Game settings
    frame_width = 640
    frame_height = 480
    lanes = 5

    # Bounding box
    x1 = 100
    y1 = 100
    x2 = 200 
    y2 = 200

    # Calculate Lane Width
    lane_width = frame_width / lanes

    while True:

        # Create game screen (rows x columns)
        frame = np.zeros((frame_height, frame_width, 3), dtype = np.uint8)

        # Calculate the x coordinate for the center of the box
        x_center = (x1 + x2) / 2

        # Get the lane index
        lane = get_lane(x_center, lane_width, lanes)

        # Calculate the car position
        car_position = calc_position(lane, lane_width, lanes)


        
# Get the Car position in Pixels
def calc_position(lane, lane_width, no_lanes):

    # Calculate the Car Position (neglect decimals)
    position = int(no_lanes * lane + lane_width / 2)

    return position


def get_lane(x_center, lane_width, no_lanes):

    # Return the index of the lane
    lane = int((x_center / lane_width))
    # Ensure that lane is not greater than last valid lane
    lane = min(lane, no_lanes - 1)

    return lane  

if __name__ == "__main__":
    main()