import random as rand
import cv2 as cv
from lanes import get_lane_center_x


class Item:
    def __init__(self, lane, speed, top_pos, bottom_pos, frame_width, num_lanes):
        self.speed = speed
        self.lane = lane
        self.frame_width = frame_width
        self.num_lanes = num_lanes
        # appear in a single row at once
        self.position = top_pos - rand.randint(1, 100)
        self.bottom_pos = bottom_pos
        self.active = True
        # x is fixed for the item's lifetime (lane doesn't change)
        self.x = get_lane_center_x(self.lane, self.frame_width, self.num_lanes)

    def step(self):
        """Move the item down the screen; deactivate once it passes the bottom."""
        if self.position >= self.bottom_pos:
            self.active = False
        else:
            self.position += self.speed

    def collided(self, lane, mcqueen_y, vulnerable, tolerance=30):
        """Same lane + close enough in y + McQueen is currently vulnerable."""
        if not vulnerable:
            return False
        if self.lane != lane:
            return False
        return abs(self.position - mcqueen_y) <= tolerance


class Tire(Item):
    def collision_action(self, points, penalty):
        points -= penalty
        self.active = False
        return points

    def show(self, frame):
        center = (self.x, int(self.position))
        cv.circle(frame, center, 10, (10, 10, 10), 3)
        cv.circle(frame, center, 7, (140, 140, 140), -1)
        return frame


class Nitro(Item):
    def collision_action(self, points, reward):
        points += reward
        self.active = False
        return points

    def show(self, frame):
        top_left = (self.x - 12, int(self.position) - 12)
        bottom_right = (self.x + 12, int(self.position) + 12)
        cv.rectangle(frame, top_left, bottom_right, (0, 200, 200), -1)
        return frame