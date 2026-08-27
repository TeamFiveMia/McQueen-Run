from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolov8n.pt")
    model.train(
        data="C:/Users/a/Desktop/Coding/M.I.A/McQueen-Run/yolo model/src/data.yaml", 
        epochs=50, 
        imgsz=640, 
        device=0,
        workers=2,   # CRITICAL: Forces single-threaded loading to protect your 8GB RAM
        batch=16,    # Your 10GB VRAM can comfortably handle standard batch sizes
        cache=False  # CRITICAL: Prevents YOLO from loading images into RAM
    )