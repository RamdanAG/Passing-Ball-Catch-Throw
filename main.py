# main.py
import cv2
import time
from hand_utils import detect_hands, get_hand_center_and_state, draw_hand_overlay
from ball import Ball
import config
from utils import distance

# inisialisasi kamera & window
cap = cv2.VideoCapture(0)
cv2.namedWindow("Passing Bola Catch & Throw", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Passing Bola Catch & Throw", config.FRAME_WIDTH, config.FRAME_HEIGHT)

# buat bola di tengah layar
ball = Ball(config.FRAME_WIDTH // 2, config.FRAME_HEIGHT // 2)

# menyimpan posisi sebelumnya tiap tangan untuk hitung velocity (x,y)
prev_positions = {"Left": None, "Right": None}
last_time = time.time()

print("Press ESC to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # resize frame sesuai config supaya semua threshold konsisten
    frame = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))
    h, w, _ = frame.shape

    results = detect_hands(frame)

    # reset visual cue tiap frame
    ball.is_glowing = False

    # default: jika bola belum dipegang siapa pun, biarkan free (bisa di-catch)
    # proses tangan terdeteksi
    if results.multi_hand_landmarks and results.multi_handedness:
        # zip memastikan kita ambil hand_landmarks + handedness bersamaan
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label  # "Left" / "Right"
            (hx, hy), is_closed = get_hand_center_and_state(
                hand_landmarks, w, h, config.CLOSED_DISTANCE, config.CLOSED_FINGER_THRESHOLD
            )

            # gambar overlay tangan
            draw_hand_overlay(frame, hand_landmarks, label, "Closed" if is_closed else "Open")

            # visual cue: kalau tangan dekat bola -> glow
            if ball.check_in_range((hx, hy)):
                ball.is_glowing = True

            # ==== Catch logic ====
            # Jika bola tidak dipegang siapapun, dan tangan tertutup + dekat -> catch
            if not ball.held:
                if is_closed and ball.check_in_range((hx, hy)):
                    ball.catch(label, (hx, hy))
                    # simpan prev_positions untuk hand ini (dipakai saat lempar)
                    prev_positions[label] = (hx, hy)
                    # after catching, skip further checks for this frame
                    continue

            # ==== If this hand is holders ====
            if ball.holder == label and ball.held:
                # Jika tangan masih closed -> tetap keep, bola mengikuti tangan (smooth)
                if is_closed:
                    ball.hold_follow((hx, hy))   # smoothing follow
                else:
                    # tangan buka -> release (lempar) berdasarkan gerakan tangan
                    prev = prev_positions.get(label)
                    ball.release((hx, hy), prev)
                    # update prev_positions after release
                    prev_positions[label] = (hx, hy)

            # Update prev_positions tiap tangan tiap frame (dipakai untuk kecepatan)
            prev_positions[label] = (hx, hy)

    # update dynamic physics (kalau tidak dipegang)
    ball.update(w, h)

    # jika bola sedang dipegang tapi holder terdeteksi hilang (misal tangan menghilang),
    # kita tetap biarkan bola attached hingga dilepas
    # draw ball terakhir
    ball.draw(frame)

    cv2.imshow("Passing Bola Catch & Throw", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
