"""
Controls:
    - Move the mouse left/right over the window to steer.
    - Press 'b' to toggle the boost visual on/off.
    - Press 'q' to quit.
"""

import cv2
import numpy as np

from lanes import FRAME_WIDTH, FRAME_HEIGHT, NUM_LANES, draw_track
from McQueen import McQueen


# def _mouse_callback(event, x, y, flags, param):
#     """Uses the mouse as a stand-in for the hand gesture x-position."""
#     param["mouse_x"] = x


def main():
    cap = cv2.VideoCapture(0)
    mcqueen = McQueen(NUM_LANES, FRAME_WIDTH, FRAME_HEIGHT)

    window_name = "Track Layout Test - Rewan's Part"
    cv2.namedWindow(window_name)
    # mouse_state = {"mouse_x": FRAME_WIDTH // 2}
    # cv2.setMouseCallback(window_name, _mouse_callback, mouse_state)

    print("Move your MOUSE left/right over the window to simulate the hand's x-position.")
    print("Press 'b' to toggle boost visual. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
           
            frame = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
        else:
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

     
        mcqueen.update_lane(mouse_state["mouse_x"])
       

        frame = draw_track(frame, NUM_LANES)
        frame = mcqueen.draw(frame)

        cv2.putText(frame, f"Lane: {mcqueen.current_lane}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()