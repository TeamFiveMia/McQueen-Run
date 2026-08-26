import cv2 as cv



def main():

   ...


def calc_position(lane, frame_width, no_lanes):

    # Calculate lane width
    lane_width = frame_width / no_lanes
    # Calculate the Car Position
    position = no_lanes * lane + lane_width / 2


def get_lane(x_center, frame_width, no_lanes):

    # Calculate the lane width
    lane_width = frame_width / no_lanes
    # Return the index of the lane
    lane = int((x_center / lane_width))
    # Ensure that lane is not greater than last valid lane
    lane = min(lane, no_lanes - 1)

    return lane  

if __name__ == "__main__":
    main()