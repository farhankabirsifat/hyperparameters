import cv2
import time
import serial
from ultralytics import YOLO

# Load YOLOv8
model = YOLO("yolov8n.pt")

# Set up Arduino serial (change COM port if needed)
arduino = serial.Serial("COM13", 9600, timeout=1)

# Camera setup
cams = {
    "North": cv2.VideoCapture(0),
    "South": cv2.VideoCapture(1),
    "East":  cv2.VideoCapture(2),
    "West":  cv2.VideoCapture(3)
}

# Optional: Reduce resolution
for cam in cams.values():
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

ROI = (200, 100, 500, 400)
step = 0

# State machine variables
state = "IDLE"
current_dir = None
phase_start = time.monotonic()
green_duration = 5  # default
phase = "GREEN"

# Send command to Arduino
def send_command(cmd):
    print(f">>> Sending to Arduino: {cmd}")
    arduino.write((cmd + "\n").encode())

def detect_vehicles(direction, cam):
    ret, frame = cam.read()
    count = 0
    if not ret:
        return direction, 0, None

    results = model(frame, verbose=False)
    boxes = results[0].boxes

    for box in boxes:
        cls = int(box.cls[0])
        if cls in [2, 3, 5, 7]:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            if ROI[0] < cx < ROI[2] and ROI[1] < cy < ROI[3]:
                count += 1
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, model.names[cls], (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Draw ROI and count
    cv2.rectangle(frame, (ROI[0], ROI[1]), (ROI[2], ROI[3]), (255, 0, 0), 2)
    cv2.putText(frame, f"Count: {count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    return direction, count, frame

try:
    while all(cam.isOpened() for cam in cams.values()):
        counts = {}
        frames = {}

        # Step 1: Detect vehicles in all directions
        for direction, cam in cams.items():
            d, count, frame = detect_vehicles(direction, cam)
            counts[d] = count
            frames[d] = frame

        # Step 2: Display all camera feeds
        for direction, frame in frames.items():
            if frame is not None:
                cv2.imshow(f"{direction} Camera", frame)

        print(f"\n[STEP {step}] Vehicle counts:")
        for direction in ["North", "South", "East", "West"]:
            print(f"  {direction}: {counts.get(direction, 0)}")

        now = time.monotonic()

        # Step 3: Traffic signal logic (non-blocking)
        if state == "IDLE":
            current_dir = max(counts, key=counts.get)
            vehicle_count = counts[current_dir]
            green_duration = max(5, min(30, 5 + vehicle_count * 2))

            dir_code = current_dir[0].upper()
            send_command(f"G_{dir_code}")
            phase = "GREEN"
            phase_start = now
            state = "RUNNING"

        elif state == "RUNNING":
            elapsed = now - phase_start

            if phase == "GREEN" and elapsed >= green_duration:
                send_command(f"Y_{current_dir[0].upper()}")
                phase = "YELLOW"
                phase_start = now

            elif phase == "YELLOW" and elapsed >= 3:
                send_command(f"R_{current_dir[0].upper()}")
                state = "IDLE"  # go back to choosing new direction

        step += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    for cam in cams.values():
        cam.release()
    arduino.close()
    cv2.destroyAllWindows()
