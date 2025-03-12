import cv2
import os
from PIL import Image

# Giriş ve çıkış klasörleri
input_folder = "ogrenci_fotograflari"
output_folder = "kirpilmis_fotograflar"

# OpenCV yüz tanıma modeli (Haar Cascade kullanıyoruz)

#face_cascade = cv2.CascadeClassifier("/home/pardus/Masaüstü/deneme/haarcascade_frontalface_default.xml")

# Yukarıdaki kullanım yanlıştır. Çünkü kullanıcılar bu programı farklı klasörlerde ve hatta farklı işletim sistemlerinde
# kullanabilir. zaten bu main dosyası ile haarcascade_frontalface_default.xml dosyası aynı klasörde, o zaman onu
# uzaklarda aramana gerek yok, sadece dosyanın ismini yazman yeterli. Her nedense çoğu program yazanlar bu hatayı yapar.
# Ama bu programı farklı insanların kullanacağını ve farklı makienlerde çalışacağını da düşünmek gerekir.

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Hedef boyutlar
target_size = (133, 171)
min_size_kb = 15
max_size_kb = 150

# Çıkış klasörünü oluştur
os.makedirs(output_folder, exist_ok=True)

# Fotoğrafları işle
try:
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
    # Terminal ekranında emoji kullanımını tavsiye etmem ama sen bilirsin :D

except Exception as error:
    # Burada iki önemli değişken bulunuyor.
    # Biri error diğer ise error_hata_ismi. Peki neye yarıyor bunlar?
    # error: Hatayı otomatik bir şekilde açıklar.
    # error_hata_ismi: bu ise hatanın ismini tutar
    # İf else yapısını kullanarak kendi hata mesajını veya otomatik hata mesajını yazdırabilirsin.

    error_hata_ismi = type(error).__name__

    if error_hata_ismi == "FileNotFoundError": # Eğer bu hatayı veriyorsa otomatik mesaj verecektir
        print(error)
    else:
        print(f"Bilinemeyen Hata! {error_hata_ismi}") # Ama bilinemeyen hata ise, yani beklemediğimiz bir hata. o zaman hatanın ismini nazikçe verir.

    # Ama istersen bu if else yapısını siler ve sadece aşağıdaki kodu kullanırsın
    #print(f"{error} Hata:{error_hata_ismi}") 
    # Ve ya sadece
    #print(error)