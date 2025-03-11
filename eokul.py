import cv2
import os
from PIL import Image

# Giriş ve çıkış klasörleri
input_folder = "ogrenci_fotograflari"
output_folder = "kirpilmis_fotograflar"

# OpenCV yüz tanıma modeli (Haar Cascade kullanıyoruz)
face_cascade = cv2.CascadeClassifier("/home/pardus/Masaüstü/deneme/haarcascade_frontalface_default.xml")


# Hedef boyutlar
target_size = (133, 171)
min_size_kb = 15
max_size_kb = 150

# Çıkış klasörünü oluştur
os.makedirs(output_folder, exist_ok=True)

# Fotoğrafları işle
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".png", ".jpeg")):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Yüz algılama için gri tonlamaya çevir

        # Yüzü algıla
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        if len(faces) > 0:
            # İlk algılanan yüzü al (genellikle en büyük yüz)
            x, y, w, h = faces[0]

            # Kırpma alanını genişlet (biraz baş ve çene de dahil olsun)
            padding_w = int(w * 0.5)
            padding_h = int(h * 0.7)

            x1 = max(x - padding_w, 0)
            y1 = max(y - padding_h, 0)
            x2 = min(x + w + padding_w, img.shape[1])
            y2 = min(y + h + padding_h, img.shape[0])

            img_cropped = img[y1:y2, x1:x2]
        else:
            # Yüz bulunamazsa resmi olduğu gibi kullan
            img_cropped = img

        # Fotoğrafı 133x171 boyutuna getir
        img_resized = cv2.resize(img_cropped, target_size, interpolation=cv2.INTER_LANCZOS4)

        # JPEG olarak kaydet (Boyutu optimize et)
        output_filename = os.path.splitext(filename)[0] + ".jpg"
        output_path = os.path.join(output_folder, output_filename)

        quality = 95  # Başlangıç sıkıştırma kalitesi

        while True:
            # Pillow ile kaliteyi ayarla ve kaydet
            img_pil = Image.fromarray(cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB))
            img_pil.save(output_path, format="JPEG", quality=quality)

            file_size_kb = os.path.getsize(output_path) / 1024  # KB cinsinden dosya boyutu

            # Boyut kontrolü
            if min_size_kb <= file_size_kb <= max_size_kb:
                break
            elif file_size_kb > max_size_kb:
                quality -= 5  # Büyükse kaliteyi düşür
            else:
                quality += 5  # Küçükse kaliteyi artır

            # Kalite çok düşerse döngüyü durdur
            if quality < 10:
                break

print("✅ Tüm fotoğraflar yüzü merkeze alınarak kırpıldı, boyutlandırıldı ve optimize edildi!")
