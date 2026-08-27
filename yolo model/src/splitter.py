import os
import random
import shutil
from collections import defaultdict


DATASET_SOURCE_DIR = os.path.join("extracted_frames")
TRAIN_DIR = os.path.join("yolo model", "data", "train1")
VAL_DIR = os.path.join("yolo model", "data", "validation2")
TRAIN_RATIO = 0.8  


if not os.path.exists(DATASET_SOURCE_DIR):
    raise FileNotFoundError(f"Cannot find '{DATASET_SOURCE_DIR}'. Ensure you run this script from your main root workspace folder.")


for base_path in [TRAIN_DIR, VAL_DIR]:
    if os.path.exists(base_path):
        shutil.rmtree(base_path)
    os.makedirs(os.path.join(base_path, "images"))
    os.makedirs(os.path.join(base_path, "labels"))


prefix_groups = defaultdict(list)
all_files = set(os.listdir(DATASET_SOURCE_DIR))


images = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

valid_pairs_count = 0
missing_labels_count = 0

for img_name in images:
    base_name, _ = os.path.splitext(img_name)
    lbl_name = f"{base_name}.txt"
    
    
    if lbl_name not in all_files:
        missing_labels_count += 1
        continue
        
    
    prefix = img_name.split("_frame_")[0] if "_frame_" in img_name else base_name
        
    prefix_groups[prefix].append((img_name, lbl_name))
    valid_pairs_count += 1


all_prefixes = list(prefix_groups.keys())
random.seed(42)
random.shuffle(all_prefixes)

split_idx = int(len(all_prefixes) * TRAIN_RATIO)
train_prefixes = all_prefixes[:split_idx]
val_prefixes = all_prefixes[split_idx:]


def distribute_data(prefixes, destination_root):
    count = 0
    for prefix in prefixes:
        for img_name, lbl_name in prefix_groups[prefix]:
            shutil.copy(os.path.join(DATASET_SOURCE_DIR, img_name), os.path.join(destination_root, "images", img_name))
            shutil.copy(os.path.join(DATASET_SOURCE_DIR, lbl_name), os.path.join(destination_root, "labels", lbl_name))
            count += 1
    return count

train_copied = distribute_data(train_prefixes, TRAIN_DIR)
val_copied = distribute_data(val_prefixes, VAL_DIR)

print("Dataset Split Completed Successfully!")
print(f"Total verified pairs: {valid_pairs_count} | Unlabeled skipped: {missing_labels_count}")
print(f"Train pairs: {train_copied} | Validation pairs: {val_copied}")