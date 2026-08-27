"""
Represents the player-controlled car. It tracks the "Steer" hand
gesture every frame and snaps to the matching lane (no click needed).

How to use this module (for the rest of the team):
    1. Each frame, call:  mcqueen.update_lane(hand_x_pixels)
        hand_x_pixels = x-coordinate (in pixels) of the center of
         the detected "Palm" bounding box from the YOLO model
         (Joudy & Omar's module).
        If YOLO gives a normalized value (0 to 1), convert it first:
             hand_x_pixels = normalized_x_center * FRAME_WIDTH
    2. Then call:  mcqueen.draw(frame)
       This updates the smooth movement AND draws the car.
       Always call update_lane() first, then draw(), every frame.
"""

import cv2
import numpy as np

from lanes import FRAME_WIDTH, FRAME_HEIGHT, NUM_LANES, get_lane_index, get_lane_center_x


class McQueen:
    def init(self, num_lanes=NUM_LANES, frame_width=FRAME_WIDTH,
                 frame_height=FRAME_HEIGHT, smooth=True):
        self.num_lanes = num_lanes
        self.frame_width = frame_width
        self.frame_height = frame_height

        self.current_lane = num_lanes // 2      
        self.car_width=40
        self.car_height=60
        self.y = frame_height - self.car_height - 20  

        # smoothing = car glides between lanes instead of jumping instantly
        # (looks better on camera )
        self.smooth = smooth
        self.display_x = float(get_lane_center_x(self.current_lane, frame_width, num_lanes))
        self.smooth_speed = 0.35  

        self.is_boosting = False  

    def update_lane(self, hand_x_pixels: float):
        """Update which lane McQueen should be in, based on the hand's x-position."""
        self.current_lane = get_lane_index(hand_x_pixels, self.frame_width, self.num_lanes)

    def start_boost(self):
        """Turn on boost visuals (call this when the Kachow Boost gesture is detected)."""
        self.is_boosting = True

    def end_boost(self):
        """Turn off boost visuals (call this when the boost window ends)."""
        self.is_boosting = False

    def _update_smoothing(self):
        """Move display_x a little closer to the target lane's center each frame."""
        target_x = get_lane_center_x(self.current_lane, self.frame_width, self.num_lanes)
        if self.smooth:
            self.display_x += (target_x - self.display_x) * self.smooth_speed
        else:
            self.display_x = target_x

    def get_x_center(self) -> int:
        """Return McQueen's current x-position on screen (after smoothing)."""
        return int(self.display_x)

    def draw(self, frame: np.ndarray) -> np.ndarray:
        """Update smooth position and draw McQueen's car icon on the frame."""
        self._update_smoothing()
        x_center = self.get_x_center()

        top_left = (x_center - self.car_width // 2, self.y)
        bottom_right = (x_center + self.car_width // 2, self.y + self.car_height)

        # gold when boosting, red normally
        color = (0,215,255) if self.is_boosting else (0,0,255)
        cv2.rectangle(frame, top_left, bottom_right, color,-1)
        cv2.rectangle(frame, top_left, bottom_right, (0,0,0), 2)   # black outline

        # small white "windshield" so it reads as a car, not just a box
        windshield_top = (x_center - 12, self.y + 8)
        windshield_bottom = (x_center + 12, self.y + 24)
        cv2.rectangle(frame, windshield_top, windshield_bottom, (255,255,255),-1)


        # motion trail behind the car while boosting (bonus visual flair)
        if self.is_boosting:
            for i in range(1, 4):
                trail_y = self.y + self.car_height + (i * 10)
                cv2.rectangle(
                    frame,
                    (x_center - self.car_width // 2 + i * 3, trail_y),
                    (x_center + self.car_width // 2 - i * 3, trail_y + 6),
                    (0, 215, 255),
                    -1
                )

        return frame