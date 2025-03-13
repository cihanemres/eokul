import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QTextEdit
from PyQt6.QtGui import QFont
import eokul_backend  # Backend modülünü içe aktarıyoruz

class EokulFotoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("e-Okul Fotoğraf Düzenleme")
        self.setGeometry(300, 200, 500, 400)

        layout = QVBoxLayout()
        
        # Başlık
        self.title_label = QLabel("📸 e-Okul Fotoğraf Düzenleme")
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(self.title_label)
        
        # Kullanıcı Kılavuzu
        self.guide_text = QTextEdit()
        self.guide_text.setText(
            "Nasıl Kullanılır?\n\n"
            "1️⃣ 'Göz At' butonuna tıklayın ve fotoğrafların olduğu klasörü seçin.\n"
            "2️⃣ 'Dönüştür' butonuna tıklayın, fotoğraflar düzenlenip aynı klasörde 'kirpilmis_fotograflar' içine kaydedilecektir.\n"
            "3️⃣ İşlem tamamlandığında sizi bilgilendireceğiz!"
        )
        self.guide_text.setReadOnly(True)
        layout.addWidget(self.guide_text)
        
        # Göz At Butonu
        self.browse_button = QPushButton("📂 Göz At")
        self.browse_button.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px;")
        self.browse_button.clicked.connect(self.open_folder)
        layout.addWidget(self.browse_button)
        
        # Dönüştür Butonu
        self.convert_button = QPushButton("🔄 Dönüştür")
        self.convert_button.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px; border-radius: 5px;")
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self.process_images)
        layout.addWidget(self.convert_button)
        
        self.setLayout(layout)
        
        self.selected_folder = None

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Fotoğraf Klasörünü Seç")
        if folder:
            self.selected_folder = folder
            self.convert_button.setEnabled(True)  # Klasör seçildikten sonra dönüştürme butonu açılır

    def process_images(self):
        if self.selected_folder:
            eokul_backend.process_photos(self.selected_folder)
            self.guide_text.setText("✅ Fotoğraflar başarıyla düzenlendi ve 'kirpilmis_fotograflar' klasörüne kaydedildi!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EokulFotoApp()
    window.show()
    sys.exit(app.exec())