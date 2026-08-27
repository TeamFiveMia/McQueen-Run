import cv2
import numpy as np

LANE_LINE_COLOR =(255, 255, 255)
LANE_LINE_THICKNESS = 2


def get_lane_boundaries(frame_width, num_lanes):    
    lanes = []
    lane_width = frame_width / num_lanes
    for i in range(num_lanes):
        x_start = int(i * lane_width)
        x_end = int((i + 1) * lane_width)
        lanes.append((x_start, x_end))
    return lanes


def get_lane_index(x_position, frame_width, num_lanes):
    # convert hand's x position into a lane number
    lane_width = frame_width / num_lanes
    lane_index = int(x_position // lane_width)
    # keep it inside the valid lane range
    return max(0, min(lane_index, num_lanes - 1))


def get_lane_center_x(lane_index, frame_width, num_lanes):
    # center x of a lane, used to place McQueen in the middle of it
    lane_width = frame_width / num_lanes
    return int(lane_index * lane_width + lane_width / 2)


def draw_track(frame, num_lanes, color=LANE_LINE_COLOR, thickness=LANE_LINE_THICKNESS):
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]
    lanes = get_lane_boundaries(frame_width, num_lanes)

    for (x_start, x_end) in lanes[1:]:
        cv2.line(frame, (x_start, 0), (x_start, frame_height), color, thickness)

    return frame