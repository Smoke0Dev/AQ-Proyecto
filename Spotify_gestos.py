import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
ultima_accion = 0

def contar_dedos(hand_landmarks):
    dedos_arriba = 0
    tips = [8, 12, 16, 20]

    # Pulgar
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        dedos_arriba += 1

    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            dedos_arriba += 1

    return dedos_arriba

while True:
    ret, frame = cap.read()
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
                pyautogui.press('playpause')
                ultima_accion = ahora

            elif dedos == 1 and ahora - ultima_accion > 2:
                print("Siguiente canción")
                pyautogui.press('nexttrack')
                ultima_accion = ahora

            elif dedos == 2 and ahora - ultima_accion > 2:
                print("Canción anterior")
                pyautogui.press('prevtrack')
                ultima_accion = ahora

    cv2.imshow("Control Spotify", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
