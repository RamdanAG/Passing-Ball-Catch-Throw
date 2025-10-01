# hand_utils.py
import cv2
import mediapipe as mp
from utils import distance

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Inisialisasi Mediapipe Hands (max 2 tangan)
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.6)

def detect_hands(frame):
    """Proses frame dan return results Mediapipe"""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return hands.process(rgb)

def get_hand_center_and_state(hand_landmarks, frame_w, frame_h, closed_dist_thresh, closed_count_thresh):
    """
    Return: (cx, cy), is_closed
    - cx,cy : posisi titik referensi tangan (landmark 9 = pangkal jari tengah)
    - is_closed : boolean, apakah tangan dianggap mengepal
    """
    cx = int(hand_landmarks.landmark[9].x * frame_w)
    cy = int(hand_landmarks.landmark[9].y * frame_h)

    # Cek jari yg dekat ke telapak
    tips = [4, 8, 12, 16, 20]
    closed_count = 0
    for tip in tips:
        tx = int(hand_landmarks.landmark[tip].x * frame_w)
        ty = int(hand_landmarks.landmark[tip].y * frame_h)
        if distance((tx, ty), (cx, cy)) < closed_dist_thresh:
            closed_count += 1

    is_closed = closed_count >= closed_count_thresh
    return (cx, cy), is_closed

def draw_hand_overlay(frame, hand_landmarks, label, state_text):
    """Gambar landmark dan label di frame"""
    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cx = int(hand_landmarks.landmark[9].x * frame.shape[1])
    cy = int(hand_landmarks.landmark[9].y * frame.shape[0])
    cv2.putText(frame, f"{label} ({state_text})", (cx - 50, cy - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
