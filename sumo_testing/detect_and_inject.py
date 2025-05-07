import cv2
from ultralytics import YOLO

# Load YOLOv8
model = YOLO("yolov8n.pt")

# Connect to four cameras
cams = {
    "North": cv2.VideoCapture(0),
    "South": cv2.VideoCapture(1),
    "East":  cv2.VideoCapture(2),
    "West":  cv2.VideoCapture(3)
}

# Define ROI bounds if needed (optional: tune for each camera)
ROI = (200, 100, 500, 400)  # (xmin, ymin, xmax, ymax)

step = 0

while all(cam.isOpened() for cam in cams.values()):
    counts = {}

    for direction, cam in cams.items():
        ret, frame = cam.read()
        # frame = cv2.resize(frame, (640, 480))
        if not ret:
            continue

        # Run detection
        results = model(frame, verbose=False)
        boxes = results[0].boxes
        count = 0

        for box in boxes:
            cls = int(box.cls[0])
            if cls in [2, 3, 5, 7]:  # car, motorbike, bus, truck
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                # Optional: Apply region filter
                if ROI[0] < cx < ROI[2] and ROI[1] < cy < ROI[3]:
                    count += 1

                # Draw box
                color = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, model.names[cls], (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                cv2.rectangle(frame, (ROI[0], ROI[1]), (ROI[2], ROI[3]), (255, 0, 0), 2)

                # cv2.putText(frame, f"Count: {count}", (10, 30),
                #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Show frame
        cv2.imshow(f"{direction} Camera", frame)
        counts[direction] = count

    # Print vehicle counts
    print(f"\n[STEP {step}] Vehicle counts:")
    for direction, count in counts.items():
        print(f"  {direction}: {count}")

    step += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release all cameras
for cam in cams.values():
    cam.release()
cv2.destroyAllWindows()
