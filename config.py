# config.py
# Atur ukuran window / frame
FRAME_WIDTH = 960
FRAME_HEIGHT = 720

# Bola
BALL_RADIUS = 30
BALL_COLOR = (0, 0, 255)    # BGR (merah)
GLOW_COLOR = (0, 255, 0)    # hijau untuk visual cue

# Jarak tangkap (pixel)
CATCH_DISTANCE = 110   # jarak agar bola bisa "dicapai" tangan (naikkan kalau susah ditangkap)

# Deteksi tangan closed/open
CLOSED_FINGER_THRESHOLD = 2  # minimal jari yang dekat ke telapak untuk dianggap mengepal
CLOSED_DISTANCE = 80         # threshold jarak jari->telapak (pixel)

# Physics / animasi
THROW_MULTIPLIER = 0.9   # seberapa kuat lempar (kalikan dari kecepatan tangan)
GRAVITY = 1.0            # gravitasi menambah vy per frame
FRICTION = 0.995         # pengurangan kecepatan setiap frame
HOLD_SMOOTH = 0.3        # smoothing saat bola mengikuti tangan (0..1), makin kecil makin halus

# Kecepatan minimum agar bola dianggap "bergerak" (untuk menghindari jitter)
MIN_VELOCITY = 0.5
