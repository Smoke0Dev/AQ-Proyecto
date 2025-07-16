import cv2
import mediapipe as mp

# Inicializar Mediapipe manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Captura de la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Voltear imagen horizontalmente
    frame = cv2.flip(frame, 1)

    # Convertir a RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar con Mediapipe
    resultado = hands.process(rgb)

    # Crear ventana negra o azul según se detecte una mano
    if resultado.multi_hand_landmarks:
        color = (255, 0, 0)  # Azul
    else:
        color = (0, 0, 0)    # Negro

    # Crear una pantalla del color elegido
    pantalla = cv2.rectangle(frame.copy(), (0, 0), (frame.shape[1], frame.shape[0]), color, -1)

    # Mostrar
    cv2.imshow("Detector de Mano", pantalla)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
