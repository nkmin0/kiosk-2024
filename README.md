# kiosk-2024
2024년 메이커즈 키오스크 프로젝트

## YOLOv5 모델로 객체인식하기

### 1. yolo모델 불러오기

```
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
```
vscode 터미널에서 위 코드 실행

![image](https://github.com/user-attachments/assets/7d605706-f055-4277-bf26-c72c898795aa)

git clone을 하면 위 그림같이 다양한 폴더가 생긴다. 이 yolov5 폴더안에 train, vaild 폴더를 넣어야지 학습을 할 수 있다.

### 2. 데이터 수집 및 라벨링

#### 데이터 수집

모델 학습을 위한 학습데이터를 수집해야 한다. 만약 동영상을 찍은 뒤 프레임별로 나누어 이미지 데이터를 수집한다면 위 Img_extraction.py를 통해 이미지 분할을 하면 된다.

```python
start_min = 0
start_sec = 0

finish_min = 5
finish_sec = 0

tic = 0.5        # tic 초에 1 장 찍기

video_num = 6

#########################################

video_path = f"D:/KIOSK_dataset/sensor_image_{video_num}.mp4"
# 영상 경로

img_path = "C:/Users/user/Desktop/kiosk/temp_dataset"
# 분할된 이미지가 저장 될 공간 (임시 폴더를 만들어 저장하는것을 추천)
```

#### 데이터 라벨링 

라벨링 툴을 써서 class 라벨링을 해줘야 한다.

https://github.com/heartexlabs/labelImg

https://makesense.ai/

이런 툴 쓰면 되는데 여기서는 https://makesense.ai/만 설명

![image](https://github.com/user-attachments/assets/a2663687-f2bf-46f1-8be5-c0d67570d060)

오른쪽 아래 Get Started 누르고 라벨링 해야하는 이미지 모두 넣은 뒤 Object Detection 누르면 라벨링을 시작할 수 있다.

![image](https://github.com/user-attachments/assets/86454cad-7262-40e2-a82f-37f1c20511c5)

Object Detection을 누르면 이런 화면이 뜨는데 

![image](https://github.com/user-attachments/assets/5c69d465-a840-45ea-ba50-d61e50961e72)

이런 라벨링할 목록을 미리 만들어두고 Load labels From file 을 눌러 불러오는것을 추천한다. 여러 이미지 파일에 대해 라벨링을 할때 다시 이미지를 불러오게 되면 라벨링 적는 순서에 따라 클래스가 꼬여버려서.....

![image](https://github.com/user-attachments/assets/520693d7-5f41-4bbc-9125-ff4527b79987)

그 다음에는 위 사진처럼 모든 객체에 대해 바운딩 박스를 그려주고 오른쪽에서 어떤 클래스인지를 골라주면 된다.


![image](https://github.com/user-attachments/assets/803d4988-9945-4acc-a55d-c64d1a43767a)

라벨링을 다 하면 왼쪽위 탭에서 Action -> Export Annotations 누르고

![image](https://github.com/user-attachments/assets/1702d7ab-0b73-4320-bf0c-d3d6b50f6ef0)

YOLO 체크해서 Export

#### 이미지 분할 (test, train, vaild)

위에 split_folder.py를 통해 만들 수 있음

![image](https://github.com/user-attachments/assets/cf116ea0-62c9-426a-afd9-b05ae912992c)

이런식으로 dataset에 모아두고 코드 돌리면 설정한 비율에 따라 이미지랑 라벨 데이터가 나뉜다.

그리고 여기서 train이랑 vaild를 복사해서 yolov5 폴더 안에 넣어주면 된다.

#### data.yaml 만들어주기

![image](https://github.com/user-attachments/assets/0a774ab5-0304-46d9-ab34-10311fcb3b8a)

이 그림처럼 yolov5안에 data 폴더에 data.yaml이라는 파일을 만들어 줘여한다. (vscode에서 하면 편함)

![image](https://github.com/user-attachments/assets/43d92ed9-7678-4cbe-8f64-08193a7d01ea)

이 코드처럼 train 이랑 vaild 폴더 경로 적어주고

앞서 라벨링 했던 목록 txt파일이랑 똑같은! 순서로 만들어주면 된다. nc는 클래스 개수
```


