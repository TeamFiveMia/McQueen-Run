import os
import cv2
from pathlib import Path


cwd = Path.cwd()
print(cwd)

video_path = "yolo model\\data\\video1.mp4"
# C:\Users\a\Desktop\Coding\M.I.A\McQueen-Run\yolo model\data\video1.mp4
capture = cv2.VideoCapture(video_path)


if not capture.isOpened():
    print("Error: Could not open the video.")
    exit()

output_dir = f"extracted_frames"
os.makedirs(output_dir, exist_ok=True)


return_bool, image = capture.read()
frame_count = 1
return_bool = True

while return_bool:
    
    return_bool, frame = capture.read()

    
    if not return_bool:
        break

    
    frame_filename = os.path.join(output_dir, f"frame_{frame_count:05d}.jpg")

    
    cv2.imwrite(frame_filename, frame)

    frame_count += 1


capture.release()
print(f"Finished! Successfully extracted {frame_count} frames.")
