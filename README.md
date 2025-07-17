# AQ-Proyecto
# Control de Spotify con Gestos de la Mano 🖐🎵

Este proyecto utiliza **MediaPipe**, **OpenCV** y **PyAutoGUI** para controlar la reproducción de música (como Spotify o cualquier reproductor multimedia) mediante gestos de la mano detectados por la cámara web.

## 🧠 ¿Cómo funciona?

El programa detecta tu mano y cuenta cuántos dedos están extendidos. Dependiendo del número de dedos levantados, se ejecutan las siguientes acciones usando atajos del teclado:

- **0 dedos** → Reproducir / Pausar
- **1 dedo** → Siguiente canción
- **2 dedos** → Canción anterior

> Para evitar múltiples activaciones por segundo, se establece un retardo de 2 segundos entre cada acción.

## 📦 Requisitos

Python 3.7 o superior.

Instala las dependencias con:

```bash
pip install opencv-python mediapipe pyautogui
