import cv2
import os
import numpy as np

# 포스터 저장 폴더
save_folder = 'posters'

# ORB 초기화
orb = cv2.ORB_create()

# 이미지의 특징을 추출하는 함수
def extract_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    return keypoints, descriptors

# 폴더 내의 모든 이미지의 특징을 미리 추출하여 저장
def extract_features_from_folder(folder):
    features = {}
    for img_file in os.listdir(folder):
        if img_file.endswith('.jpg'):
            img_path = os.path.join(folder, img_file)
            이미지 = cv2.imread(img_path)
            _, descriptors = extract_features(이미지)
            features[img_file] = descriptors
    return features

# 이미지를 검색하여 유사한 이미지를 찾는 함수
def search_similar_images(query_image_path, folder, features):
    query_image = cv2.imread(query_image_path)
    _, query_descriptors = extract_features(query_image)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    results = []

    for img_file, descriptors in features.items():
        if descriptors is not None and query_descriptors is not None:
            matches = bf.match(query_descriptors, descriptors)
            matches = sorted(matches, key=lambda x: x.distance)
            results.append((img_file, len(matches)))

    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results

# 폴더 내 모든 이미지의 특징 추출
features = extract_features_from_folder(save_folder)

# 검색할 이미지 경로
query_image_path = 'posters/poster_0.jpg'  # 검색할 이미지의 경로를 지정

# 유사한 이미지 검색
similar_images = search_similar_images(query_image_path, save_folder, features)

# 유사한 이미지 출력
for img_file, num_matches in similar_images[:5]:  # 유사한 상위 5개 이미지 출력
    img_path = os.path.join(save_folder, img_file)
    이미지 = cv2.imread(img_path)
    cv2.imshow('img', 이미지)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(f"{img_file}: {num_matches} matches")
