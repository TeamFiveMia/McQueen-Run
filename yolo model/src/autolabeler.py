import os
import cv2
import mediapipe as mp

input_dir = "data\\data\\train"
OUTPUT_DIR = "data\\labels"
os.makedirs(OUTPUT_DIR, exist_ok=True)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True, 
    max_num_hands=2, 
    min_detection_confidence=0.5
)