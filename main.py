import random as rand
import McQueen
import lanes
import obstacles as ob
import numpy as np      # Importing numpy
import cv2 as cv        # Import open cv library
import useNitro         # Import Module that contains Nitro boost feature
import Steer         # Import Module that contains palm steering feature
from ultralytics import YOLO # Import the YOLO models (YOU ONLY LOOK ONCE)

# Start the Web Cam
camera = cv.VideoCapture(0)
# Get the actual DIMENSIONS of the camera
FRAME_WIDTH = int(camera.get(cv.CAP_PROP_FRAME_WIDTH))
FRAME_HEIGHT = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))

# Load the YOLO model
model = YOLO("")    # TODO (Model type)

speed = 5 # The speed at which items move
top_pos = FRAME_HEIGHT # Position at the top of the screen
bottom_pos = 0 # Position at the bottom of the screen

NUM_ITEMS = 10 # Number of items at any time
NUM_LANES = 5 # Number of lanes ( MODIFIED )
items = [] # The list of all items
LANE_WIDTH = FRAME_WIDTH / lanes

points = 0 # Initializing points to 0
PENALTY = 10 # The penalty of points when colliding with the tires
REWARD = 5 # The reward points when collecting with nitro

# Get McQueen's data, from Rewan's code
McQueen.pos = ...       
McQueen.lane = lanes // 2      # (MODIFIABLE) start at the Middle
McQueen.vulnerable = ...

# new_item: Returns a list of random items in random lanes
def new_item(number, lanes):
    for _ in range(number):
        type = rand.randint(1,2)
        lane = rand.randint(0, lanes)

        if type == 1:
            return ob.Tire(lane, speed, top_pos, bottom_pos)

        else:
            return ob.Nitro(lane, speed, top_pos, bottom_pos)

# Handle losing the game
def game_lost():
    ...
    # Closing the windows
    camera.release()
    cv.destroyAllWindows()


def main():
    # Create the items
    for _ in range(10):
        items.append(new_item(NUM_ITEMS, lanes))

    # Start the game
    while True:
        # Read the Camera frame
        loaded, frame = camera.read()
        # Check Reading the Camera successfully
        if not loaded:
            print("Failed to read from the camera")

        # Run the Model
        detection = model(frame)

        # Check if game is still on
        if points < 0:
            game_lost()

        # Check for the palm gesture with highest confidence
        palm = Steer.get_palm(detection)

        # If Palm was detected
        if palm is not None:
            # Get the coordinates of the Bounding box
            x1, y1, x2, y2 = palm
            # Calculate the center of the box
            x_center = (x1 + x2) / 2
            # Get the current lane
            McQueen.update_lane(x_center, LANE_WIDTH, lanes)
            
            
        # Calculate the current X position
        McQueen.pos = Steer.calc_position(McQueen.lane, LANE_WIDTH)

        # Check if Nitro is Working   
        string, isNitro = useNitro.response()

        if not isNitro:
            
            for item in items:
                item.step()
                if item.active == False:
                    item = new_item(NUM_ITEMS, lanes)
                if item.collided(item, McQueen.lane, McQueen.pos, McQueen.vulnerable):
                    item.collision_action(points, penalty=PENALTY, reward=REWARD)
            if detection == "peace_sign":
                useNitro.after_detection()


        

        # Show the frame
        frame = lanes.draw_track(frame, NUM_LANES)
        frame = McQueen.draw(frame)
        
        cv.putText(frame, f"Lane: {McQueen.current_lane}", (10, 30),
            cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv.imshow("McQueen Run", frame)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        


if __name__ == "__main__":
    main()