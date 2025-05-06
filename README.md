# 🚦 AI-Based Real-Time Traffic Light Control System

A smart traffic management system that dynamically controls traffic lights based on real-time vehicle detection using YOLOv8, Python, and Arduino. This project aims to reduce congestion, improve fuel efficiency, and enhance road safety in urban intersections.

---

## 📌 Problem Statement

Traditional traffic lights operate on static timers and do not adapt to real-time traffic flow, leading to:
- Increased traffic congestion and longer wait times
- Fuel wastage and higher emissions
- Inefficient utilization of road capacity
- Lack of affordable and scalable smart solutions for urban and semi-urban areas

---

## 💡 Solution Approach

Our system provides a low-cost, AI-driven solution by:
- Using YOLOv8 to detect vehicles in real-time from live camera feeds
- Calculating vehicle density per lane
- Prioritizing the lane with the highest traffic and allocating green light time accordingly
- Controlling traffic signals through an Arduino using serial communication from the Python application

---

## 🤖 AI Model Details

**Model:** YOLOv8 (You Only Look Once - Version 8)  
**Frameworks Used:**  
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- OpenCV for image processing
- NumPy, time, serial (Python standard libraries)

**Dataset:**  
- Pre-trained COCO dataset (for object detection including cars, buses, trucks, etc.)

**Detection Flow:**  
1. Capture video frames
2. Detect and count vehicles in each lane
3. Select the lane with the highest count
4. Send control signal to Arduino to switch traffic lights

---

## ⚙️ Deployment Process

### 🔧 Hardware Requirements
- ESP32 or Arduino Uno
- 4 Traffic LEDs (Red, Yellow, Green x4)
- Jumper wires and breadboard
- Webcam or IP camera

### 🧠 Software Setup
1. Clone this repo:
   ```bash
   git clone https://github.com/farhankabirsifat/hyperparameters.git
   cd ai-traffic-light-system