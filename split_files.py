import os
import shutil

def split_files(path):
    # 원본 폴더 경로
    source_folder = path

    # labels 폴더와 images 폴더 경로
    labels_folder = os.path.join(source_folder, 'labels')
    images_folder = os.path.join(source_folder, 'images')

    # 폴더가 존재하지 않으면 생성
    os.makedirs(labels_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)

    # 원본 폴더의 파일 목록 가져오기
    files = os.listdir(source_folder)

    # 파일 분류 및 이동
    for file in files:
        if file.endswith('.txt'):
            shutil.move(os.path.join(source_folder, file), os.path.join(labels_folder, file))
        elif file.endswith('.jpg'):
            shutil.move(os.path.join(source_folder, file), os.path.join(images_folder, file))

    print(f"{path} : 파일 분류 완료.")


file_path = "C:/2024GEP/dataset" # 각자 경로에 맞추어 수정
split_files(f"{file_path}/test")
split_files(f"{file_path}/train")
split_files(f"{file_path}/valid")