import cv2 as cv



def main():

   ...




def get_lane(x_center, frame_width, no_lanes):

    # Calculate the lane width
    lane_width = frame_width / no_lanes
    # Return the index of the lane
    return int((x_center / lane_width) - 1)

if __name__ == "__main__":
    main()