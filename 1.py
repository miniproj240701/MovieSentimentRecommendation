import cv2
import os
import numpy as np
from tqdm import tqdm

def extract_features(image_path):
    img = cv2.imread(image_path, 0)
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(img, None)
    return des

def match_features(des1, des2):
    if des1 is None or des2 is None:
        return 0
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    similarity = len(matches) / max(len(des1), len(des2))
    return similarity

def find_similar_images(query_image, poster_folder, top_n=5):
    query_features = extract_features(query_image)
    similarities = []

    total_images = 572  # poster_0.jpg부터 poster_571.jpg까지
    for i in tqdm(range(total_images), desc="Processing images"):
        filename = f"poster_{i}.jpg"
        image_path = os.path.join(poster_folder, filename)
        if os.path.exists(image_path):
            features = extract_features(image_path)
            similarity = match_features(query_features, features)
            similarities.append((filename, similarity))
        else:
            print(f"Warning: {filename} not found")

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]

# 사용 예
poster_folder = 'posters'
query_image = os.path.join(poster_folder, 'poster_0.jpg')  # 예: poster_0.jpg를 쿼리 이미지로 사용
top_n = 5

similar_images = find_similar_images(query_image, poster_folder, top_n)
print("\nTop 5 similar images:")
for filename, similarity in similar_images:
    print(f"{filename}: Similarity {similarity:.4f}")