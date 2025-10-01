# ball.py
import cv2
import numpy as np
from config import BALL_RADIUS, BALL_COLOR, GLOW_COLOR, CATCH_DISTANCE, THROW_MULTIPLIER, GRAVITY, FRICTION, HOLD_SMOOTH, MIN_VELOCITY
from utils import distance, lerp

class Ball:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.holder = None   # "Left" / "Right" / None
        self.held = False
        self.is_glowing = False

    def check_in_range(self, hand_pos):
        return distance((self.x, self.y), hand_pos) < CATCH_DISTANCE

    def catch(self, hand_label, hand_pos):
        """Tangkap bola: set holder dan matikan velocity"""
        self.holder = hand_label
        self.held = True
        self.vx = 0.0
        self.vy = 0.0
        self.x, self.y = float(hand_pos[0]), float(hand_pos[1])

    def release(self, hand_pos, prev_pos):
        """
        Lepas bola: hitung velocity berdasarkan gerakan tangan (hand_pos - prev_pos)
        - prev_pos bisa None -> jika None beri velocity minimal
        """
        self.holder = None
        self.held = False
        if prev_pos is None:
            self.vx, self.vy = 0.0, -5.0
        else:
            dx = hand_pos[0] - prev_pos[0]
            dy = hand_pos[1] - prev_pos[1]
            # Kalikan dengan multiplier; invert dy supaya mengangkat ketika gerakan ke atas
            self.vx = dx * THROW_MULTIPLIER
            self.vy = dy * THROW_MULTIPLIER
            # Jika sangat kecil -> berikan minimal impulse
            if abs(self.vx) < MIN_VELOCITY and abs(self.vy) < MIN_VELOCITY:
                self.vy = -6.0

    def update(self, frame_w, frame_h):
        """Update posisi bola jika tidak dipegang (physics sederhana), atau smoothing jika dipegang"""
        if self.held and self.holder is not None:
            # Saat dipegang, posisi di-handle oleh main loop (mengikuti tangan).
            return

        # Jika tidak dipegang -> physics
        self.x += self.vx
        self.y += self.vy

        # gravity
        self.vy += GRAVITY

        # friction
        self.vx *= FRICTION
        self.vy *= FRICTION

        # batas layar dan pantulan sederhana
        r = BALL_RADIUS
        if self.x < r:
            self.x = r
            self.vx = -self.vx * 0.6
        if self.x > frame_w - r:
            self.x = frame_w - r
            self.vx = -self.vx * 0.6
        if self.y > frame_h - r:
            self.y = frame_h - r
            self.vy = -abs(self.vy) * 0.6  # pantul sedikit
            # kalau pantulan kecil -> stop di tanah
            if abs(self.vy) < 1.0:
                self.vy = 0.0

    def hold_follow(self, hand_pos):
        """Bola mengikuti tangan dengan smoothing (lerp)"""
        target_x, target_y = float(hand_pos[0]), float(hand_pos[1])
        self.x = lerp(self.x, target_x, HOLD_SMOOTH)
        self.y = lerp(self.y, target_y, HOLD_SMOOTH)

    def draw(self, frame):
        """Gambar bola. Kalau glowing -> gambar overlay hijau transparan"""
        if self.is_glowing:
            overlay = frame.copy()
            cv2.circle(overlay, (int(self.x), int(self.y)), BALL_RADIUS, GLOW_COLOR, -1)
            alpha = 0.4
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        # gambar outline bola (agar selalu terlihat)
        cv2.circle(frame, (int(self.x), int(self.y)), BALL_RADIUS, BALL_COLOR, -1)
        cv2.circle(frame, (int(self.x), int(self.y)), BALL_RADIUS, (0,0,0), 2)  # outline
