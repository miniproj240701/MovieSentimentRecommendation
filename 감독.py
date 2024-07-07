import requests
import os

# Create a directory to save the images
os.makedirs('directors', exist_ok=True)

# List of director names and image URLs
directors = {
    "이창동": "https://search.pstatic.net/common?type=b&size=216&expire=1&refresh=true&quality=100&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F56%2F201610111052357171.jpg",
    "홍상수": "https://search.pstatic.net/common?type=b&size=216&expire=1&refresh=true&quality=100&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F63%2F201404171451029001.jpg",
    "김기덕": "https://search.pstatic.net/common?type=b&size=216&expire=1&refresh=true&quality=100&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F70%2F202012211223198861.png",
    "박찬욱": "https://search.pstatic.net/common?type=b&size=216&expire=1&refresh=true&quality=100&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F30%2F201405092025014301.jpg",
    "봉준호": "https://search.pstatic.net/common?type=b&size=216&expire=1&refresh=true&quality=100&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F189%2F201710111116464471.jpg",
    "김지운": "https://search.pstatic.net/common?type=b&size=216&expire=1&refresh=true&quality=100&direct=true&src=http%3A%2F%2Fsstatic.naver.net%2Fpeople%2F80%2F201611041816343891.jpg"
}

# Function to download and save images
def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

# Download each image
for name, url in directors.items():
    image_path = os.path.join('directors', f"{name}.jpg")
    download_image(url, image_path)
