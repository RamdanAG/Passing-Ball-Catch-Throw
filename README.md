# 🏐 Passing Bola Catch & Throw (Hand Tracking + OpenCV + Mediapipe)

Proyek ini adalah simulasi **passing bola virtual** menggunakan **webcam** dengan **tracking tangan (Mediapipe)**.  
Kamu bisa **menangkap bola** dengan mengepal tangan di dekat bola, lalu **melempar** dengan membuka tangan sambil menggerakkan tangan.  
Fitur ini bisa digunakan untuk eksperimen interaktif, game gesture, atau latihan pemrograman computer vision.

---

## ✨ Fitur
- 🎥 **Real-time hand tracking** menggunakan [Mediapipe Hands](https://developers.google.com/mediapipe).
- 🖐️ Deteksi **tangan terbuka / mengepal**.
- 🏀 Bola bisa:
- **Ditangkap** (catch) jika tangan mengepal dekat bola.
- **Dilempar** (throw) sesuai gerakan tangan saat membuka.
- **Dipantulkan** dengan physics sederhana (gravitasi, friction).
- 🔵 **Visual cue (glow)**: bola menyala hijau jika tangan berada dalam jangkauan tangkap.

---

## 📂 Struktur Folder
- main.py # Entry point aplikasi
- ball.py # Class Ball: logic bola (catch, throw, update physics)
- hand_utils.py # Utilitas deteksi & overlay tangan
- utils.py # Fungsi helper (distance, lerp)
- config.py # Konfigurasi (ukuran frame, physics, threshold, warna bola)
- README.md # Dokumentasi


---

## ⚙️ Instalasi
1. Clone repo ini:
   ```
   git clone https://github.com/username/passing-bola.git
   cd passing-bola
   ```
   ```
   pip install opencv-python mediapipe numpy
   ```
   ```
   python main.py
   ```
