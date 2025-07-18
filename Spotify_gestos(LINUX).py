import cv2
import mediapipe as mp
import time
import os

# Inicializar MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Funciones para controlar Spotify con playerctl
def play_pause():
    os.system("playerctl -p spotify play-pause")

def next_track():
    os.system("playerctl -p spotify next")

def previous_track():
    os.system("playerctl -p spotify previous")

# Captura de video
cap = cv2.VideoCapture(0)
ultima_accion = 0

# Función para contar dedos levantados
def contar_dedos(hand_landmarks):
    dedos_arriba = 0
    tips = [8, 12, 16, 20]

    # Pulgar
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        dedos_arriba += 1

    # Otros dedos
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            dedos_arriba += 1

    return dedos_arriba

# Bucle principal
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al acceder a la cámara")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            dedos = contar_dedos(hand)

            cv2.putText(frame, f"Dedos: {dedos}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            ahora = time.time()

            if dedos == 0 and ahora - ultima_accion > 2:
                print("Play/Pause")
                play_pause()
                ultima_accion = ahora

            elif dedos == 1 and ahora - ultima_accion > 2:
                print("Siguiente canción")
                next_track()
                ultima_accion = ahora

            elif dedos == 2 and ahora - ultima_accion > 2:
                print("Canción anterior")
                previous_track()
                ultima_accion = ahora

    cv2.imshow("Control Spotify", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

