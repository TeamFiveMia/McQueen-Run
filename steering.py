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

    hand_center_x = 150
    x1 = int(hand_center_x - 50)
    x2 = int(hand_center_x + 50)

    # Calculate Lane Width
    Lane_width = frame_width / lanes

    while True:

        # Create game screen (rows x columns)
        frame = np.zeros((frame_height, frame_width, 3), dtype = np.uint8)

        # Calculate the x coordinate for the center of the box
        x_center = (x1 + x2) / 2

        # Get the lane index
        lane = get_lane(x_center, Lane_width, lanes)

        # Calculate the car position
        car_position = calc_position(lane, Lane_width)

        # Draw lane boundaries
        for i in range(1, lanes):
            x = int(i * Lane_width)

            cv.line(frame, (x,0), (x,frame_height), (255, 255, 255), 2)

        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        cv.circle(frame, (int(x_center), int((y1 + y2) / 2)), 5, (0, 255, 0), -1)

        # Draw McQueen
        car_width = 60
        car_height = 40

        car_left = int(car_position - car_width / 2)
        car_top = frame_height - 80
    
        cv.rectangle(
            frame,
            (car_left, car_top),
            (car_left + car_width, car_top + car_height),
            (0, 0, 255),
            -1
        )
    
        # Display information
        cv.putText(
            frame,
            f"Hand X: {int(x_center)}",
            (10, 30),
            cv.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
    
        cv.putText(
            frame,
            f"Lane: {lane}",
            (10, 60),
            cv.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
    
        cv.imshow("Movement Test", frame)
    
        # Press ESC to quit
        key = cv.waitKey(30)

        if key == ord('a'):
            hand_center_x -= 10

        elif key == ord('d'):
            hand_center_x += 10

        elif key == 27:
            break

        x1 = int(hand_center_x - 50)
        x2 = int(hand_center_x + 50)
    cv.destroyAllWindows()
    
         
         


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

if __name__ == "__main__":
    main()