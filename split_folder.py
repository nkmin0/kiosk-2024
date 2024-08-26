import os
import shutil
import random

# 경로 설정
data_path = 'C:/Users/user/Desktop/kiosk/dataset'  # 모든 이미지와 라벨 파일이 모여 있는 폴더 경로
output_path = 'C:/Users/user/Desktop/kiosk/custom_dataset'

train_path = f'{output_path}/train'
valid_path = f'{output_path}/valid'
test_path = f'{output_path}/test'

# 비율 설정 (예: 70% train, 20% valid, 10% test)
train_ratio = 0.8
valid_ratio = 0.15
test_ratio = 0.05

# 데이터 리스트 가져오기
file_list = [f for f in os.listdir(f'{data_path}/images') if f.endswith('.jpg')]
print(file_list)
# 데이터 섞기
random.shuffle(file_list)

# 데이터 나누기
total_files = len(file_list)
train_files = file_list[:int(total_files * train_ratio)]
valid_files = file_list[int(total_files * train_ratio):int(total_files * (train_ratio + valid_ratio))]
test_files = file_list[int(total_files * (train_ratio + valid_ratio)):]

# 폴더 생성
os.makedirs(f'{train_path}/images', exist_ok=True)
os.makedirs(f'{train_path}/labels', exist_ok=True)
os.makedirs(f'{valid_path}/images', exist_ok=True)
os.makedirs(f'{valid_path}/labels', exist_ok=True)
os.makedirs(f'{test_path}/images', exist_ok=True)
os.makedirs(f'{test_path}/labels', exist_ok=True)

def move_files(file_list, destination_folder):
    for file_name in file_list:
        # 이미지 파일 복사
        shutil.copy(os.path.join(f'{data_path}/images', file_name), os.path.join(f'{destination_folder}/images', file_name))
        # 라벨 파일 복사
        label_file = file_name.replace('.jpg', '.txt')
        if os.path.exists(os.path.join(f'{data_path}/labels', label_file)):
            shutil.copy(os.path.join(f'{data_path}/labels', label_file), os.path.join(f'{destination_folder}/labels', label_file))

# 파일 이동
move_files(train_files, train_path)
move_files(valid_files, valid_path)
move_files(test_files, test_path)

print("데이터 분할 완료!")
