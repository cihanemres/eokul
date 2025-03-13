import cv2
import os
from PIL import Image

def process_photos(input_folder):
    output_folder = os.path.join(input_folder, "kirpilmis_fotograflar")
    os.makedirs(output_folder, exist_ok=True)

    # Haarcascade dosyasının yolu
    haarcascade_path = os.path.join(os.path.dirname(__file__), "haarcascade_frontalface_default.xml")
    face_cascade = cv2.CascadeClassifier(haarcascade_path)

    target_size = (133, 171)
    min_size_kb = 15
    max_size_kb = 150

    try:
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                img_path = os.path.join(input_folder, filename)
                img = cv2.imread(img_path)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

                if len(faces) > 0:
                    x, y, w, h = faces[0]
                    padding_w = int(w * 0.5)
                    padding_h = int(h * 0.7)
                    x1 = max(x - padding_w, 0)
                    y1 = max(y - padding_h, 0)
                    x2 = min(x + w + padding_w, img.shape[1])
                    y2 = min(y + h + padding_h, img.shape[0])
                    img_cropped = img[y1:y2, x1:x2]
                else:
                    img_cropped = img

                img_resized = cv2.resize(img_cropped, target_size, interpolation=cv2.INTER_LANCZOS4)
                output_filename = os.path.splitext(filename)[0] + ".jpg"
                output_path = os.path.join(output_folder, output_filename)
                
                quality = 95
                while True:
                    img_pil = Image.fromarray(cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB))
                    img_pil.save(output_path, format="JPEG", quality=quality)
                    file_size_kb = os.path.getsize(output_path) / 1024
                    
                    if min_size_kb <= file_size_kb <= max_size_kb:
                        break
                    elif file_size_kb > max_size_kb:
                        quality -= 5
                    else:
                        quality += 5

                    if quality < 10:
                        break
        
        print("✅ Fotoğraflar başarıyla düzenlendi!")
    except Exception as error:
        print(f"❌ Hata oluştu: {error}")
