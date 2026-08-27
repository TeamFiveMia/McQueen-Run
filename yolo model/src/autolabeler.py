import os
import cv2 as cv
import mediapipe as mp

input_dir = "data\\data\\train"
output = "data\\labels"
os.makedirs(output, exist_ok=True)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True, 
    max_num_hands=2, 
    min_detection_confidence=0.5
)

for file in os.listdir(output):
    if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    path_img = os.path.join(input_dir, file)
    img = cv.imread(path_img, cv.IMREAD_COLOR_RGB)

    if not img:
        continue

    height, width, _ = img.shape

    

