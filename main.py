import random as rand
import obstacles as ob
import numpy as np      # Importing numpy
import cv2 as cv        # Import open cv library
import useNitro         # Import Module that contains Nitro boost feature
import steering         # Import Module that contains palm steering feature
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

number = 10 # Number of items at any time
lanes = 5 # Number of lanes ( MODIFIED )
items = [] # The list of all items

points = 0 # Initializing points to 0
PENALTY = 10 # The penalty of points when colliding with the tires
REWARD = 5 # The reward points when collecting with nitro

# Get McQueen's data, from Rewan's code
mcqueen.pos = ...
mcqueen.lane = ...
mcqueen.vulnerable = ...

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
        items.append(new_item(number, lanes))

    # Start the game
    while True:
        # Read the Camera frame
        loaded, frame = camera.read()
        # Check Reading the Camera successfully
        if not loaded:
            print("Failed to ")

        # Run the Model
        detection = model(frame)

        # Check if game is still on
        if points < 0:
            game_lost()

            # Check for the palm gesture

        palm
        # Check if Nitro is Working   
        string, isNitro = useNitro.response()
        if not isNitro:
            
            for item in items:
                item.step()
                if item.active == False:
                    item = new_item(number, lanes)
                if item.collided(item, mcqueen.lane, mcqueen.pos, mcqueen.vulnerable):
                    item.collision_action(points, penalty=PENALTY, reward=REWARD)
            if detection == "peace_sign":
                useNitro.after_detection()
        


if __name__ == "__main__":
    main()