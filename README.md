# Open-CV
## 1st stage : Using live.py file
Live Face Detection using OpenCV 

This project demonstrates **real-time face detection** using OpenCV and a pre-trained Haar Cascade classifier.  
The webcam is used to capture live video frames, and faces are detected and highlighted with green rectangles (BGR format).
---
### 📌 Requirements
- Python 3.x  
- OpenCV (`cv2`)
  
Install dependencies:
```bash
pip install opencv-python
```
# Drowsiness Detection using OpenCV & Dlib
## 2nd Stage: Using liv3.py file

This project detects **drowsiness and eye blinks** in real time using a webcam.  
It uses:
- **Dlib’s 68 facial landmarks predictor** to track eye movements  
- **OpenCV** for video capture and visualization  
- A custom logic to determine if the user is **Active**, **Drowsy**, or **Sleeping**

---

## 📌 Requirements
- Python 3.x  
- OpenCV  
- Dlib  
- imutils  
- NumPy  

Install dependencies:
```bash
pip install opencv-python dlib imutils numpy
```
# Drowsiness Detection using GSR sensor connected in arduino 
##3rd stage: using Driver_Drowiness_Detection_Arduino.ino file 


This Arduino code reads values from a GSR (Galvanic Skin Response) sensor connected to pin A0 and calculates both the averaged
sensor reading and an estimated human skin resistance, then prints these values over serial output.

# Drowsiness Detection using GSR sensor connected in arduino Uno +Buzzer
## 4 th stage: using Drowiness_Detection_Final_Arduino.ino file 
This reads the GSR average and listens for a command from Python:

'1' → buzzer ON

'0' → buzzer OFF

# Drowsiness Detection using OpenCV & Dlib final Code 
## 5 th stage: livefinal.py file





