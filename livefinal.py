import cv2
import numpy as np
import dlib
from imutils import face_utils
import time
import serial

# ---- CONFIG ----
SERIAL_PORT = 'COM3'         # Windows example; Linux: '/dev/ttyACM0' or '/dev/ttyUSB0'
BAUD = 9600
GSR_SETPOINT = 500           # Tune this after observing your readings

# Open Arduino serial
arduino = serial.Serial(SERIAL_PORT, BAUD, timeout=0.1)
time.sleep(2)  # Allow Arduino to reset

# Camera + Dlib setup (your code)
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

sleep = drowsy = active = 0
status = ""
color = (0, 0, 0)

def compute(ptA, ptB):
    return np.linalg.norm(ptA - ptB)

def blinked(a,b,c,d,e,f):
    up = compute(b,d) + compute(c,e)
    down = compute(a,f)
    ratio = up/(2.0*down)
    if ratio > 0.25:
        return 2
    elif 0.21 < ratio <= 0.25:
        return 1
    else:
        return 0

def read_gsr_value():
    """Return latest GSR avg as int or None if not available."""
    try:
        line = arduino.readline().decode(errors='ignore').strip()
        if line:
            return int(line)
    except:
        pass
    return None

try:
    while True:
        ok, frame = cap.read()
        if not ok:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        face_frame = frame.copy()

        # Default to "Active" if no face found long enough
        for face in faces:
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            cv2.rectangle(face_frame, (x1,y1), (x2,y2), (0,255,0), 2)

            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            left_blink = blinked(landmarks[36],landmarks[37],landmarks[38],
                                 landmarks[41],landmarks[40],landmarks[39])
            right_blink = blinked(landmarks[42],landmarks[43],landmarks[44],
                                  landmarks[47],landmarks[46],landmarks[45])

            if (left_blink == 0 or right_blink == 0):
                sleep += 1; drowsy = 0; active = 0
                if sleep > 6:
                    status = "SLEEPING !!!"; color = (255,0,0)
            elif (left_blink == 1 or right_blink == 1):
                sleep = 0; active = 0; drowsy += 1
                if drowsy > 6:
                    status = "Drowsy !"; color = (0,0,255)
            else:
                drowsy = 0; sleep = 0; active += 1
                if active > 6:
                    status = "Active :)"; color = (0,255,0)

            for n in range(0, 68):
                (x,y) = landmarks[n]
                cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

        # Show status
        cv2.putText(frame, status, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.imshow("Frame", frame)
        cv2.imshow("Result of detector", face_frame)

        # ----- Read GSR -----
        gsr = read_gsr_value()
        if gsr is not None:
            # Map to binary inputs where 0 = risky
            cam_bit = 0 if status == "SLEEPING !!!" else 1
            gsr_bit = 0 if gsr < GSR_SETPOINT else 1

            # --------- PICK YOUR LOGIC ---------
            # A) NAND logic (buzzer ON if ANY input is 0; OFF only when both are 1/good)
            buzzer_on = not (cam_bit and gsr_bit)

            # B) If you want ON only when BOTH are 0, use this instead:
            # buzzer_on = (cam_bit == 0 and gsr_bit == 0)
            # -----------------------------------

            # Send command to Arduino
            arduino.write(b'1' if buzzer_on else b'0')

            # (Optional) Debug prints
            # print(f"GSR={gsr} cam_bit={cam_bit} gsr_bit={gsr_bit} buzzer={int(buzzer_on)}")

        # Exit
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break

finally:
    try:
        arduino.write(b'0')   # ensure buzzer off
    except:
        pass
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()


