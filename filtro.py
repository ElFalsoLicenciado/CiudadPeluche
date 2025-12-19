import math
import cv2 as cv
import glfw
import mediapipe as mp
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import pygame

# Variables de OpenGL
window = None

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = "El Balatreador"

# Variables de figuras
tex_floor = None


# Variables de Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)


def init_glfw():
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    return window


def setup_opengl():
    glClearColor(0.165, 0.753, 0.98, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)


    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    tex_floor = load_texture("C:/Users/User/Desktop/CiudadPeluche/res/floor4k.jpg")


def load_texture(path):
    img = Image.open(path).convert("RGB")
    img_data = img.tobytes()

    tex_id = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    glBindTexture(GL_TEXTURE_2D, tex_id)

    # Filtrado
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Envoltura (tiling)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Subir la textura
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 img.width, img.height, 0,
                 GL_RGB, GL_UNSIGNED_BYTE, img_data)

    # Crear mipmaps
    glGenerateMipmap(GL_TEXTURE_2D)

    glBindTexture(GL_TEXTURE_2D, 0)

    return tex_id


def setup_lights():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)  # Luz adicional
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Luz principal frontal
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1))

    # Luz de relleno lateral
    glLightfv(GL_LIGHT1, GL_POSITION, (1, 1, 1, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))


def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(4, 4, 8,
              0, 0, 0,
              0, 1, 0)


    glfw.swap_buffers(window)



def main():
    global window
    try:
        window = init_glfw()
    except RuntimeError as e:
        print(e)
        return

    setup_opengl()
    setup_lights()

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
        glfw.terminate()
        return

    cap.set(cv.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

    frame_count = 0
    fps_timer = glfw.get_time()

    left_index = None

    try:
        while not glfw.window_should_close(window):
            ret, frame = cap.read()
            if not ret: break

            current_frame = glfw.get_time()

            frame = cv.flip(frame, 1)

            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            # if results.multi_hand_landmarks and results.multi_handedness:
            #     for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            #         label = handedness.classification[0].label  # Clasificacion: Left o Right
            #         if label == "Left":
            #             left_index = (hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y)

            glfw.poll_events()

            if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS: break


            draw_scene()

            frame_count += 1
            current_time = glfw.get_time()

            if current_time - fps_timer >= 1.0:
                fps = frame_count / (current_time - fps_timer)
                glfw.set_window_title(window, f"{WINDOW_TITLE} - FPS: {fps:.1f}")
                frame_count = 0
                fps_timer = current_time

    except Exception as e:
        print(f" Error en el loop principal: {e}")
        import traceback
        traceback.print_exc()

    finally:
        cap.release()
        glfw.terminate()


if __name__ == "__main__":
    main()




