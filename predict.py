import cv2
import time
import torch

cap = cv2.VideoCapture(0)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/kiosk_v4.1/weights/best.pt')

#model.conf = 0.5

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
print("open")
while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read from webcam.")
        break
    results = model(img)

    img = results.render()[0]  # results.render()는 감지된 객체를 그려줌
    print(results)
    
    cv2.imshow('Webcam', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
print("close")
cv2.destroyAllWindows()
