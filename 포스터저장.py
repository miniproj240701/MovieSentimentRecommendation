import cv2
import json
import requests
import numpy as np
import os

# JSON 파일 읽기
lst = []
with open('긍부정영화정보리스트.json', encoding='utf-8') as f:
    dt = json.load(f)
    lst.append(dt)

# 포스터 저장 폴더
save_folder = 'posters'
os.makedirs(save_folder, exist_ok=True)

# 모든 포스터 다운로드 및 저장
for idx, item in enumerate(lst[0]):
    포스터 = item['포스터']
    response = requests.get(포스터)
    image_data = np.frombuffer(response.content, np.uint8)
    이미지 = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    # 이미지 파일 저장
    save_path = os.path.join(save_folder, f'poster_{idx}.jpg')
    cv2.imwrite(save_path, 이미지)

print(f"모든 포스터 이미지를 {save_folder} 폴더에 저장했습니다.")
