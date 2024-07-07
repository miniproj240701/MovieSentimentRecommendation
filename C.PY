from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
from deep_translator import GoogleTranslator

# 모델과 프로세서 로드
vit_gpt2_checkpoint = "nlpconnect/vit-gpt2-image-captioning"

vit_gpt2_model = VisionEncoderDecoderModel.from_pretrained(vit_gpt2_checkpoint)
processor = ViTImageProcessor.from_pretrained(vit_gpt2_checkpoint)
tokenizer = AutoTokenizer.from_pretrained(vit_gpt2_checkpoint)

device = "cuda" if torch.cuda.is_available() else "cpu"
vit_gpt2_model.to(device)

def generate_caption(image_path):
    # 이미지 로드 및 전처리
    image = Image.open(image_path)
    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)
    
    # 캡션 생성
    generated_ids = vit_gpt2_model.generate(pixel_values, max_length=50, num_beams=5)
    generated_caption = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return generated_caption

def translate_caption(caption, target_language='ko'):
    translated_caption = GoogleTranslator(source='auto', target=target_language).translate(caption)
    return translated_caption

# 예제 이미지 경로
image_path = 'posters/poster_571.jpg'
generated_caption = generate_caption(image_path)

# 한글로 번역
translated_caption = translate_caption(generated_caption)

print("Generated Caption:", generated_caption)
print("Translated Caption:", translated_caption)
