import cv2
import numpy as np
import os
from tqdm import tqdm
import json

def extract_features(image_path):
    img = cv2.imread(image_path)
    
    # SIFT 특징 추출
    sift = cv2.SIFT_create()
    _, des_sift = sift.detectAndCompute(img, None)
    
    # 색상 히스토그램
    hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    
    return des_sift, hist

def match_features(des1, des2, hist1, hist2):
    if des1 is None or des2 is None:
        return 0
    
    # SIFT 특징 매칭
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    
    # Lowe's ratio test with a more lenient threshold
    good_matches = [m for m, n in matches if m.distance < 0.8 * n.distance]
    sift_similarity = len(good_matches) / max(len(des1), len(des2))
    
    # 히스토그램 비교
    hist_similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    
    # 결합된 유사도
    combined_similarity = 0.7 * sift_similarity + 0.3 * hist_similarity
    
    return combined_similarity

def compare_all_images(poster_folder, top_n=10):
    total_images = 572
    all_features = {}

    for i in tqdm(range(total_images), desc="Extracting features"):
        filename = f"poster_{i}.jpg"
        image_path = os.path.join(poster_folder, filename)
        if os.path.exists(image_path):
            sift_features, hist_features = extract_features(image_path)
            all_features[filename] = (sift_features, hist_features)
        else:
            print(f"Warning: {filename} not found")

    similarities = {}

    for i in tqdm(range(total_images), desc="Comparing images"):
        filename1 = f"poster_{i}.jpg"
        if filename1 not in all_features:
            continue
        
        similarities[filename1] = []
        for j in range(total_images):
            if i == j:
                continue
            filename2 = f"poster_{j}.jpg"
            if filename2 not in all_features:
                continue
            
            similarity = match_features(all_features[filename1][0], all_features[filename2][0],
                                        all_features[filename1][1], all_features[filename2][1])
            similarities[filename1].append({"파일명": filename2, "유사도": similarity})
        
        similarities[filename1].sort(key=lambda x: x["유사도"], reverse=True)
        similarities[filename1] = similarities[filename1][:top_n]

        # 중간 결과 저장 (JSON 형식)
        if i % 10 == 0:  # 10개의 이미지를 처리할 때마다 저장
            with open('similarities_partial.json', 'w') as f:
                json.dump(similarities, f, indent=2)

    # 최종 결과 저장 (JSON 형식)
    with open('similarities_final.json', 'w') as f:
        json.dump(similarities, f, indent=2)

    return similarities

# 사용 예
poster_folder = 'posters'
top_n = 10  # 상위 10개로 증가

# 이전 결과가 있는지 확인
if os.path.exists('similarities_final.json'):
    print("Loading previous results...")
    with open('similarities_final.json', 'r') as f:
        all_similarities = json.load(f)
else:
    print("Calculating similarities...")
    all_similarities = compare_all_images(poster_folder, top_n)

# 결과 출력
for filename, similar_images in all_similarities.items():
    print(f"\nTop {top_n} similar images for {filename}:")
    for image in similar_images:
        print(f"  {image['파일명']}: Similarity {image['유사도']:.4f}")