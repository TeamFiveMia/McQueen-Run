import os
import cv2 as cv
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

CLASS_MAP = {"Palm": 0, "Peace Sign": 1}

model_path = "hand_landmarker.task"
if not os.path.exists(model_path):
    print("Downloading Hand Landmarker model...")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    urllib.request.urlretrieve(url, model_path)
    print("Download complete.")


base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.7
)

input_dir = "extracted_frames"

# os.makedirs(output, exist_ok=True)
#test_pic = "extracted_frames\\frame_00001.jpg"



# for file in os.listdir(input_dir):
# with test_pic as file:
#     # if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
#     #     continue

#     # path_img = os.path.join(input_dir, file)
#     # label

#     img = cv.imread(file, cv.IMREAD_COLOR_RGB)

#     # if not img:
#     #     return

#     height, width, _ = img.shape

#     hand_results = hands.process(img)
#     print(hand_results)




failed_pics = []

with vision.HandLandmarker.create_from_options(options) as finder:
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img_path = os.path.join(input_dir, filename)
        img = cv.imread(img_path)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        mp_img = mp.Image(mp.ImageFormat.SRGB, img)


        result = finder.detect(mp_img)
        
        if result.hand_landmarks:
        
            for lm in result.hand_landmarks:
                
                thumb_up = False
                index_up = False
                middle_up = False
                ring_up = False
                pinky_up = False

                # if lm[4].y > lm[2]:
                #     thumb_up = True

                if lm[8].y < lm[6].y:
                    index_up = True

                if lm[12].y < lm[10].y:
                    middle_up = True

                if lm[16].y < lm[14].y:
                    ring_up = True

                if lm[20].y < lm[18].y:
                    pinky_up = True

                if index_up and middle_up and ring_up and pinky_up:
                    hand = "Palm"
                elif index_up and middle_up and not ring_up and not pinky_up:
                    hand = "Peace Sign"
                else:
                    hand = None


                if hand:
                    hand = CLASS_MAP[hand]
                    x_coords = [landmark.x for landmark in lm]
                    y_coords = [landmark.y for landmark in lm]

                    x_min = min(x_coords)
                    x_max = max(x_coords)
                    y_min = min(y_coords)
                    y_max = max(y_coords)

                    #for YOLO format
                    #class_id center_x center_y width height
                    padding = 0.30  # 30% padding

                    x_min = max(0, x_min - padding * (x_max - x_min))
                    x_max = min(1, x_max + padding * (x_max - x_min))
                    y_min = max(0, y_min - padding * (y_max - y_min))
                    y_max = min(1, y_max + padding * (y_max - y_min))
                    box_w = x_max - x_min
                    box_h = y_max - y_min
                    x_center = x_min + (box_w / 2)
                    y_center = y_min + (box_h / 2)

                    txt_path = os.path.join(
                                            input_dir,
                                            os.path.splitext(filename)[0] + ".txt"
                    )
                    with open(txt_path, "w") as f:
                        f.write(f"{hand} {x_center:.6f} {y_center:.6f} {box_w:.6f} {box_h:.6f}\n")

                    print("Done labeling")
                else:
                    failed_pics.append(filename)

        else:
            failed_pics.append(filename)


with open("failed_pics.txt", "w") as f:
    for pic in failed_pics:
        f.write(f"{pic}\n")