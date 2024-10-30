import cv2                          # pip install opencv-python ultralytics pandas cvzone pyserial
from ultralytics import YOLO
import pandas as pd
from tracker import Tracker
import cvzone
import serial
import time

# Initialize serial communication with Arduino
arduino = None
try:
    # Replace 'COM3' with your Arduino port (e.g., 'COM3' or '/dev/ttyUSB0')
    # arduino = serial.Serial('COM3', 115200, timeout=1)
    time.sleep(2)  # Give time for the connection to establish
    print("Arduino connected.")
except serial.SerialException as e:
    print(f"Error connecting to Arduino: {e}")
    exit()

# Check available camera indices
index = 0
found_camera = False
max_indices = 10  # Limit to 10 attempts

index = 1
while True:
 #   cap=cv2.VideoCapture('cow1.mp4')
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Camera index {index} is not available.")
        index += 1
    else:
        print(f"Camera index {index} is available.")
        break

# Use the available camera index
cap=cv2.VideoCapture('cow1.mp4')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

model = YOLO("best.pt")  
tracker = Tracker()
cowcount = []
cy1 = 487
offset = 6

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    frame = cv2.resize(frame, (1008, 600))
    
      # Only read from Arduino if it's successfully initialized
    if arduino is not None:
        if arduino.in_waiting > 1:
            gps_data = arduino.readline().decode('utf-8').strip()
            print("GPS Data:", gps_data)  # Process GPS data as needed
    else:
        print("Arduino is not connected.")

    results = model(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    list = []

    for index, row in px.iterrows():
        x1, y1, x2, y2, _, d = map(int, row)
        list.append([x1, y1, x2, y2])
        
    bbox_list = tracker.update(list)

    for bbox in bbox_list:
        x3, y3, x4, y4, id = bbox
        cx = int(x3 + x4) // 2
        cy = int(y3 + y4) // 2

        if cy1 < (cy + offset) and cy1 > (cy - offset):
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
            cvzone.putTextRect(frame, f'{id}', (x3, y3), 1, 1)
            if id not in cowcount:
                cowcount.append(id)

    counting = len(cowcount)                                   # calculates the number of elements in the cowcount listand stores that number in the variable counting (position,rfid's,year,born date,color etc,)
    cvzone.putTextRect(frame, f'{counting}', (50, 60), 2, 2)   # This line uses the putTextRect function from the cvzone library to draw a rectangle with text on the frame.(50, 60) specifies the position (x, y coordinates) on the frame where the text will be placed.The two 2s represent the thickness and font scale of the text.
    cv2.line(frame, (5, 487), (1019, 487), (255, 0, 255), 2)   # draws a horizontal line on the frame using OpenCV's line function, line starts at the point (5, 487) and ends at (1019, 487).color of the line is specified as (255, 0, 255), which is a magenta color in BGR format (used by OpenCV).
    cv2.imshow("RGB", frame)                                   # displays the modified frame in a window titled "RGB".

    if cv2.waitKey(1) & 0xFF == ord('q'):                      # The bitwise AND operation & 0xFF is used to mask the result of waitKey to ensure that only the last 8 bits are considered. This is important because waitKey can return a larger value on some platforms, but we only need the ASCII value of the key pressed, and we want to quit, The ord function returns the ASCII value of the character 'q'. This is used to check if the pressed key is 'q'.
        break

cap.release()
cv2.destroyAllWindows()

