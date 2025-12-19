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

tex_craft_top = None
tex_craft_bottom = None
tex_craft_side = None
tex_craft_front = None


flower = [
    "---12--",
    "-13213-",
    "134312-",
    "11112--",
    "-356---",
    "---7---",
    "---7---",
    "---7---",
    "56-8-66",
    "-5-55--",
    "--565--",]

flower_colors = {
    "1": (0.929, 0.188, 0.173),
    "2": (0.608, 0.133, 0.102),
    "3": (0.749, 0.145, 0.161),
    "4": (0.455, 0.137, 0.012),
    "5": (0.125, 0.275, 0.149),
    "6": (0.149, 0.353, 0.145),
    "7": (0.29, 0.561, 0.157),
    "8": (0.169, 0.439, 0.165)

}

# Variables de animación
rotation_angle = 0.0
movement_offset = 0.0
movement_direction = 1.0

# Variables de Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# ============================================================
# GLF
# ============================================================
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
    global tex_floor
    global tex_craft_top, tex_craft_bottom, tex_craft_side, tex_craft_front

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
    tex_craft_top = load_texture("C:/Users/User/Desktop/CiudadPeluche/res/crafting_top.png")
    tex_craft_bottom = load_texture("C:/Users/User/Desktop/CiudadPeluche/res/oak_planks.png")
    tex_craft_side = load_texture("C:/Users/User/Desktop/CiudadPeluche/res/crafting_side.png")
    tex_craft_front = load_texture("C:/Users/User/Desktop/CiudadPeluche/res/crafting_front.png")


def load_texture(path):
    img = Image.open(path).convert("RGB")
    img = img.transpose(Image.ROTATE_180)
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


def update_motion(scale=1.0, chin=None):
    global rotation_angle,movement_offset, movement_direction


    rotation_angle += 5
    if rotation_angle >= 360:
        rotation_angle = 0  # Reiniciar el ángulo después de una vuelta completa


def begin_solid_draw():
    glPushAttrib(
        GL_CURRENT_BIT |
        GL_ENABLE_BIT |
        GL_LIGHTING_BIT |
        GL_TEXTURE_BIT |
        GL_LINE_BIT
    )

def end_solid_draw():
    glPopAttrib()


# ============================================================
# Dibujo de primitivas
# ============================================================

# Horizontal
# a1 = (x1, y1, z1)
# a2 = (x2, y2, z2)
#
# p1 = (x1, y1, z1)
# p2 = (x2, y1, z1)
# p3 = (x1, y2, z2)
# p4 = (x2, y2, z2)


def draw_textured_rectangle_top(p1,p2, texture=None):
    glBindTexture(GL_TEXTURE_2D, texture)


    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    glNormal3f(0.0, 0.0, -1.0)

    point1 = (p1[0], p1[1], p1[2])
    point2 = (p2[0], p1[1], p1[2])
    point3 = (p2[0], p2[1], p2[2])
    point4 = (p1[0], p2[1], p2[2])


    glTexCoord2f(0, 0); glVertex3f(*point1)
    glTexCoord2f(1, 0); glVertex3f(*point2)
    glTexCoord2f(1, 1); glVertex3f(*point3)
    glTexCoord2f(0, 1); glVertex3f(*point4)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)


# Vertical
# a1 = (x1, y1, z1)
# a2 = (x2, y2, z2)
#
# p1 = (x1, y1, z1)
# p2 = (x1, y2, z1)
# p3 = (x2, y1, z2)
# p4 = (x2, y2, z2)

def draw_textured_rectangle_side(p1, p2, texture=None):
    glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    glNormal3f(0.0, 0.0, -1.0)

    point1 = (p1[0], p1[1], p1[2])
    point2 = (p1[0], p2[1], p1[2])
    point3 = (p2[0], p2[1], p2[2])
    point4 = (p2[0], p1[1], p2[2])


    glTexCoord2f(0, 0); glVertex3f(*point1)
    glTexCoord2f(1, 0); glVertex3f(*point2)
    glTexCoord2f(1, 1); glVertex3f(*point3)
    glTexCoord2f(0, 1); glVertex3f(*point4)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)


def draw_line(p1, p2, color=(1, 0, 0), width=2.0):
    begin_solid_draw()

    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glLineWidth(width)
    glColor3f(*color)

    glBegin(GL_LINES)
    glVertex3f(*p1)
    glVertex3f(*p2)
    glEnd()

    end_solid_draw()


def draw_polygon(polygon, color=(1, 1, 1)):
    glLineWidth(1.0)
    glColor3f(*color)
    glBegin(GL_POLYGON)
    for point in polygon:
        glVertex3f(*point)
    glEnd()


def draw_pixel(x, y, size=0.05, color=(1, 0, 0)):
    polygon = [
        (x, y, 0),
        (x + size, y, 0),
        (x + size, y + size, 0),
        (x, y + size, 0),
    ]
    draw_polygon(polygon, color)


def draw_sphere(x, y, z, radius, color=(1, 1, 1)):
    begin_solid_draw()

    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glColor3f(*color)

    glPushMatrix()
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, 20, 20)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    end_solid_draw()


def draw_cone(x, y, z, base_radius, height, color=(1, 0, 0)):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(0, 0, 0, 1)
    glRotatef(-90, 1, 0, 0)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluCylinder(quad, base_radius, 0, height, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()


def draw_textured_cube(texture_top=None, texture_bottom=None, texture_side=None, texture_front=None):
        glBindTexture(GL_TEXTURE_2D, texture_front)

        glBegin(GL_QUADS)

        # Frente (z = +1)
        glColor3f(1, 1, 1)
        glTexCoord2f(0, 0); glVertex3f(-1, -1, 1)
        glTexCoord2f(1, 0); glVertex3f(1, -1, 1)
        glTexCoord2f(1, 1); glVertex3f(1, 1, 1)
        glTexCoord2f(0, 1); glVertex3f(-1, 1, 1)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)

        glBindTexture(GL_TEXTURE_2D, texture_front)
        glBegin(GL_QUADS)
        # Atrás (z = -1)
        glColor3f(1, 1, 1)

        glTexCoord2f(0, 0); glVertex3f(-1, -1, -1)
        glTexCoord2f(1, 0); glVertex3f(-1, 1, -1)
        glTexCoord2f(1, 1); glVertex3f(1, 1, -1)
        glTexCoord2f(0, 1); glVertex3f(1, -1, -1)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)

        glBindTexture(GL_TEXTURE_2D, texture_side)
        glBegin(GL_QUADS)
        # Izquierda (x = -1)
        glColor3f(1, 1, 1)
        glTexCoord2f(0, 0); glVertex3f(-1, -1, -1)
        glTexCoord2f(1, 0); glVertex3f(-1, -1, 1)
        glTexCoord2f(1, 1); glVertex3f(-1, 1, 1)
        glTexCoord2f(0, 1); glVertex3f(-1, 1, -1)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)

        glBindTexture(GL_TEXTURE_2D, texture_side)
        glBegin(GL_QUADS)
        # Derecha (x = +1)
        glColor3f(1, 1, 1)
        glTexCoord2f(0, 0); glVertex3f(1, -1, -1)
        glTexCoord2f(1, 0); glVertex3f(1, -1, 1)
        glTexCoord2f(1, 1); glVertex3f(1, 1, 1)
        glTexCoord2f(0, 1); glVertex3f(1, 1, -1)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)

        glBindTexture(GL_TEXTURE_2D, texture_top)
        glBegin(GL_QUADS)
        # Arriba (y = +1)
        glColor3f(1, 1, 1)
        glTexCoord2f(0, 0); glVertex3f(-1, 1, -1)
        glTexCoord2f(1, 0); glVertex3f(-1, 1, 1)
        glTexCoord2f(1, 1); glVertex3f(1, 1, 1)
        glTexCoord2f(0, 1); glVertex3f(1, 1, -1)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)

        glBindTexture(GL_TEXTURE_2D, texture_bottom)
        glBegin(GL_QUADS)
        # Abajo (y = -1)
        glColor3f(1, 1, 1)
        glTexCoord2f(0, 0); glVertex3f(-1, -1, -1)
        glTexCoord2f(1, 0); glVertex3f(1, -1, -1)
        glTexCoord2f(1, 1); glVertex3f(1, -1, 1)
        glTexCoord2f(0, 1); glVertex3f(-1, -1, 1)

        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)


# ============================================================
# Modelos
# ============================================================
def draw_floor():
    begin_solid_draw()

    glEnable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glColor3f(1,1,1)

    glBindTexture(GL_TEXTURE_2D, tex_floor)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-5, -0.1, -5)
    glTexCoord2f(1, 0); glVertex3f(5, -0.1, -5)
    glTexCoord2f(1, 1); glVertex3f(5, -0.1, 5)
    glTexCoord2f(0, 1); glVertex3f(-5, -0.1, 5)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)

    end_solid_draw()



def draw_flower(origin_x=0, origin_y=0, pixel_size=0.05):
    begin_solid_draw()

    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glColor3f(1,1,1)

    for y, row in enumerate(flower):
        for x, cell in enumerate(row):
            if cell != "-":
                draw_pixel(
                    origin_x + x * pixel_size,
                    origin_y - y * pixel_size,
                    pixel_size,
                    flower_colors[cell]
                )

    end_solid_draw()


def draw_chingadera():

    angle = math.sin(math.radians(30))

    color_patas = (0.776, 0.616, 0.529)
    color_cuerpo = (0.208, 0.157, 0.161)
    color_pico = (0.239, 0.231, 0.227)

    pata_x = 0.075

    eye_x = 0.07
    eye_y = 1.12
    eye_z = 0.24
    eye_size = 0.03


    # Pata izquierda
    draw_line((-pata_x, 0.1, 0), (-pata_x, 1, 0), color_patas, 3.0 )
    draw_line((-pata_x, 0.1, 0), (-pata_x+(-pata_x*angle), 0.1, 0+(0.5*angle)), color_patas, 2.5 )
    draw_line((-pata_x, 0.1, 0), (-pata_x, 0.1, 0.5*angle), color_patas, 2.5 )
    draw_line((-pata_x, 0.1, 0), (-pata_x-(-pata_x*angle), 0.1, 0+(0.5*angle)), color_patas, 2.5 )


    # Pata derecha
    draw_line((pata_x, 0.1, 0), (pata_x, 1, 0), color_patas, 3.0 )
    draw_line((pata_x, 0.1, 0), (pata_x+(pata_x*angle), 0.1, 0+(0.5*angle)), color_patas, 2.5 )
    draw_line((pata_x, 0.1, 0), (pata_x, 0.1, 0.5*angle), color_patas, 2.5 )
    draw_line((pata_x, 0.1, 0), (pata_x-(pata_x*angle), 0.1, 0+(0.5*angle)), color_patas, 2.5 )

    # Cuerpo,
    glPushMatrix()
    glScalef(1, 1, 1.5)
    draw_sphere(0, 1, 0, 0.15, color_cuerpo)
    glPopMatrix()

    # Cabeza
    glPushMatrix()
    glScalef(1, 1, 1.25)
    draw_sphere(0, 1.10, 0.15, 0.1, color_cuerpo)
    glPopMatrix()

    # Pico
    glPushMatrix()
    glTranslatef(0, 1.25, -1.05)
    glRotatef(90, 1, 0, 0)
    draw_cone(0, 1.25, 0.15, 0.05, 0.3, color_pico)
    glPopMatrix()

    # Ojos

    glPushMatrix()
    glTranslatef(eye_x, eye_y, eye_z)
    draw_sphere(0, 0, 0, eye_size, (0,0,0))
    glPopMatrix()
    glPushMatrix()
    glTranslatef(eye_x * -1, eye_y, eye_z)
    draw_sphere(0, 0, 0, eye_size, (0,0,0))
    glPopMatrix()

# ============================================================
# Mundo
# ============================================================
def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(0, 2, 5,
              0,2 , -1,
              0, 1, 0)

    draw_floor()

    glDisable(GL_LIGHTING)
    glPushMatrix()
    scale = 0.25
    glTranslatef(0, 1*scale, 0)
    glScalef(scale, scale, scale)
    draw_textured_cube(tex_craft_top, tex_craft_bottom, tex_craft_side, tex_craft_front)
    glPopMatrix()


    glPushMatrix()
    scale = 1.0
    glTranslatef(0, 1, 0)
    glRotatef(0, 0, 1, 0)
    glScalef(scale, scale, scale)
    draw_flower()
    glPopMatrix()
    glEnable(GL_LIGHTING)

    glPushMatrix()
    # scale = 0.5
    glTranslatef(0, 0.5, 2)
    glRotatef(rotation_angle, 0, 1, 0)
    # glScalef(scale, scale, scale)
    draw_chingadera()
    glPopMatrix()

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
            update_motion()


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




