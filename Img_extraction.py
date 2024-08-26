import sys
import os
import cv2
import numpy as np
import re

# 0 : 2:00
# 1 : 0:17
# 2 : 1:08
# 3 : 0:17
# 4 : 2:19
# 5 : 0:32

###########################################################
###########################################################

start_min = 0
start_sec = 0

finish_min = 5
finish_sec = 0

tic = 0.4        # tic 초에 1 장 찍기

video_num = 6

###########################################################
###########################################################

start = start_min * 60 + start_sec
finish = finish_min * 60 + finish_sec

# 각자 영상 경로에 맞추어 수정
# video_path = f"D:/KIOSK_dataset/sensor_image_{video_num}.mp4"
video_path = "C:/Users/user/Desktop/kiosk/yolov5/runs/detect/exp7/sensor_image_6.mp4"


img_path = f"D:\KIOSK_image"
os.makedirs(img_path, exist_ok=True)

try:
    video = cv2.VideoCapture(video_path)
    print('동영상 읽기 성공')
except:
    print('동영상 읽기 실패')

fps = round(video.get(cv2.CAP_PROP_FPS),0)
print(fps)

def get_name(img_path, i):
    
    name = f"video_{video_num}_{i:04d}.jpg"  # video0_0001.jpg 형식
    return name
    
start_frame = start * fps
finish_frame = finish * fps
tic_frame = tic * fps

frame_count = 0
i=1
while True:
    ret, img = video.read()  # 성공 여부(bool), 이미지
    frame_count += 1
    
    
    if not ret:  # ret이 False일 때 (파일에 문제가 있거나 동영상이 끝났을 때)
        print('이미지 읽기 실패 또는 모두 읽음')
        video.release()
        break

    if start_frame <= frame_count <= finish_frame:
        now_frame = frame_count - start_frame
        
        if now_frame % tic_frame == 0:
            name = get_name(img_path, i)
            i+=1
            print(ret, frame_count, name)
            cv2.imwrite(f"{img_path}/{name}", img)

    if finish_frame < frame_count:

        print(finish_frame, frame_count)
        video.release()
        break
