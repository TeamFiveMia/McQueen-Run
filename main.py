import random as rand
import cv2 as cv
from ultralytics import YOLO
import McQueen
import lanes
import obstacles as ob
import useNitro
import Steer

# Start the Video Capture
camera = cv.VideoCapture(0)
# Get the dimensions of the web came
FRAME_WIDTH = int(camera.get(cv.CAP_PROP_FRAME_WIDTH))
FRAME_HEIGHT = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))

# Load the model
model = YOLO("best.pt")

SPEED = 5      # Speed of objects falling
TOP_POS = 0    # Coordinates start y = 0 from up
BOTTOM_POS = FRAME_HEIGHT   # Bottom of the screen is the y-axis

NUM_ITEMS = 10   # Number of obstacles
NUM_LANES = 5    # Number of lanes (fixed :( )

PENALTY = 10
REWARD = 5

points = 0     # Score on start


def new_item(no_lanes):
    """Create a single random item (Tire or Nitro) in a random lane."""
    lane = rand.randint(0, no_lanes - 1)
    if rand.randint(1, 2) == 1:
        return ob.Tire(lane, SPEED, TOP_POS, BOTTOM_POS, FRAME_WIDTH, NUM_LANES)
    else:
        return ob.Nitro(lane, SPEED, TOP_POS, BOTTOM_POS, FRAME_WIDTH, NUM_LANES)


def game_lost(frame):
    # Output Game Over at the center of the screen
    cv.putText(frame, "GAME OVER", (FRAME_WIDTH // 2 - 150, FRAME_HEIGHT // 2 - 20),
               cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    cv.putText(frame, f"Final Score: {points}", (FRAME_WIDTH // 2 - 150, FRAME_HEIGHT // 2 + 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv.imshow("mcqueen Run", frame)
    cv.waitKey(2000)
    camera.release()
    cv.destroyAllWindows()


def main():
    global points

    mcqueen = McQueen.McQueen(NUM_LANES, FRAME_WIDTH, FRAME_HEIGHT)
    items = []
    for _ in range(NUM_ITEMS):
        items.append(new_item(NUM_LANES))

    while True:
        loaded, frame = camera.read()
        if not loaded:
            print("Failed to read from the camera")
            continue

        detection = model(frame)

        # Check for Steering 
        palm = Steer.get_palm(detection[0])
        if palm is not None:
            x1, y1, x2, y2 = palm
            x_center = (float(x1) + float(x2)) / 2
            mcqueen.update_lane(x_center)

        # Check for Boost
        peace = useNitro.get_peace(detection[0])
        if peace is not None:
            useNitro.after_detection()

        # Ends boost when time is over
        useNitro.response() 
        mcqueen.is_boosting = useNitro.boost

        # 
        for i, item in enumerate(items):
            item.step()

            if item.collided(mcqueen.current_lane, mcqueen.y, useNitro.vulnerable):
                if isinstance(item, ob.Tire):
                    points = item.collision_action(points, PENALTY)
                else:
                    points = item.collision_action(points, REWARD)
                    useNitro.nitro_add()

            if not item.active:
                items[i] = new_item(NUM_LANES)
            else:
                item.show(frame)

        # Draw track and car
        frame = lanes.draw_track(frame, NUM_LANES)
        frame = mcqueen.draw(frame)
        frame = cv.flip(frame, 1)

        cv.putText(frame, f"Lane: {mcqueen.current_lane}", (10, 30),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv.putText(frame, f"Score: {points}", (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv.putText(frame, f"Nitro: {useNitro.nitro}", (10, 90),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 215, 255), 2)

        cv.imshow("mcqueen Run", frame)

        if points < 0:
            game_lost(frame)
            return

        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            camera.release()
            cv.destroyAllWindows()
            return


if __name__ == "__main__":
    main()