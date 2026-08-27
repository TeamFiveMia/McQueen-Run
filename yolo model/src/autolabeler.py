import os
import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


CLASS_MAP = {"Palm": 0, "Peace Sign": 1}

input_dir = "data\\data\\train"
output = "data\\labels"
os.makedirs(output, exist_ok=True)
test_pic = "extracted_frames\\frame_00001.jpg"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True, 
    max_num_hands=2, 
    min_detection_confidence=0.5
)

# for file in os.listdir(input_dir):
with test_pic as file:
    # if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
    #     continue

    # path_img = os.path.join(input_dir, file)
    # label

    img = cv.imread(file, cv.IMREAD_COLOR_RGB)

    # if not img:
    #     return

    height, width, _ = img.shape

    hand_results = hands.process(img)
    print(hand_results)



