import cv2
import time
import torch

# 웹캠 열기
cap = cv2.VideoCapture(2)
# YOLOv5 모델 로드 (파인튜닝된 모델)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/kiosk_v4.1/weights/best.pt')

# 감지할 최소 신뢰도 임계값 설정
#model.conf = 0.5  # 원하는 신뢰도 수준으로 설정 (예: 0.5)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
print("open")
while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read from webcam.")
        break

    # 모델을 사용하여 객체 감지 수행
    results = model(img)

    # 결과를 이미지에 그리기
    img = results.render()[0]  # results.render()는 감지된 객체를 그려줌
    #print(results)
    
    # 이미지 보여주기
    cv2.imshow('Webcam', img)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠과 창 닫기
cap.release()
print("close")
cv2.destroyAllWindows()
