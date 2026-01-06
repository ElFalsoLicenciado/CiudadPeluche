import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import pygame


from Alive.Minion import Minion
from Alive.Fish import Fish
from Alive.Ferrari import Ferrari
from Alive.Chingadera import Chingadera
from Street.building import Building
from Street.flower import Flower
from Street.light_pole import LightPole
from Street.Tree import Tree
from Street.Oxxo import Oxxo
from Street.craftin_table import Crafting
from Street.umbrella import Umbrella
from Util.Landmarks import HAND_CONNECTIONS

square_t = 0.0
square_offset_x = 0.0
square_offset_z = 0.0

# Modelo para landmarks
MODEL_PATH = r"C:\Users\User\Desktop\CiudadPeluche2\LL\hand_landmarker.task"

# Variables asbestianas
minion_t = 0.0
minion_t_y = 0.0
minion_t_x = 0.0
minion_motion = 1

fish_angle = 0.0

ahh_fish_t = 0.0
ahh_fish_x = 0.0
ahh_fish_y = 0.0
ahh_fish_angle = 0.0
ahh_fish_motion = 1

damnn_angle = 0.0

floating_table_offset = 0.0
floating_table_motion = 1


w, h = 800, 600
# Ángulo de rotación inicial
angle = 0.0
# Zoom inicial
zoom = 4
# Altura inicial
height = 7
# Declaración del rastreador de landmarks
tracker = None

normal_building = Building(1.5)
mini_building = Building(1)

normal_minion = Minion(0.5)
normal_fish = Fish(0.1)
normal_ferrari = Ferrari(0.6)
normal_tree = Tree(1.2)
big_tree = Tree(2)
normal_light_pole = LightPole(0.75)
normal_flower = Flower()
normal_chingadera = Chingadera()
normal_crafting = None
normal_umbrella = Umbrella()

normal_oxxo = Oxxo(1)
mini_oxxo = Oxxo(0.7)

def init():
    glClearColor(0, 0, 0.6, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

def reshape(width, frame_height):
    global w, h
    w, h = width, max(frame_height, 1)
    glViewport(0, 0, w, h)

def minion_jump():
    global minion_t, minion_motion, minion_t_y, minion_t_x


    minion_t -= 0.01 * minion_motion
    minion_t_y = -8*(minion_t**2)-4*minion_t
    minion_t_x -= 0.01 *minion_motion

    if minion_motion == 1:
        if minion_t_x <= -3:
            minion_motion *= -1

        if minion_t <= -0.5:
            minion_t = 0.0

    if minion_motion == -1:
        if minion_t_x >= 0:
            minion_motion *= -1

        if minion_t >= 0:
            minion_t = -0.5

def fish_rotation():
    global fish_angle

    fish_angle += 5

    if fish_angle >= 360:
        fish_angle = 0



def parametric_square(scale=1.0):
    global square_t, square_offset_x, square_offset_z

    if square_t == 0:
        if square_offset_x < 1.0*(scale-0.5):
            square_offset_x += 0.01*scale
        else: square_t = 90

    if square_t == 90:
        if square_offset_z < 1.0*(scale-0.5):
            square_offset_z += 0.01*scale
        else: square_t = 180

    if square_t == 180:
        if square_offset_x > 0.0:
            square_offset_x -= 0.01*scale
        else:
            square_t = 270

    if square_t == 270:
        if square_offset_z > 0.0:
            square_offset_z -= 0.01*scale
        else:
            square_t = 0

# Generar texturas
def load_texture(path):
    img = Image.open(path)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL usa origen abajo
    img_data = img.convert("RGBA").tobytes()

    width, tex_height = img.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA,
        width, tex_height, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, img_data
    )

    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id

# Para evitar que mediapipe ensucie las texturas importadas, si no se usa, las texturas se pintan del color de las líneas de las manos
def begin_textured_draw(tex_id):
    glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT | GL_TEXTURE_BIT | GL_LIGHTING_BIT)
    glDisable(GL_LIGHTING)            # para que no se “mate” la textura
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glColor4f(1.0, 1.0, 1.0, 1.0)     # <- IMPORTANTÍSIMO: quita el tinte azul

# Usar al terminar de dibujar la textura
def end_textured_draw():
    glBindTexture(GL_TEXTURE_2D, 0)
    glPopAttrib()

# Dibujar mano en escena
def draw_hand_2d(hands):
    # Dibujar en coordenadas de pantalla (0..w, 0..h)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, w, h, 0)  # ojo: y hacia abajo para parecerse a OpenCV

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glPointSize(6)
    glLineWidth(2)

    for hand in hands:
        pts = [(lm[0]*w, lm[1]*h) for lm in hand]

        # puntos
        glBegin(GL_POINTS)
        glColor3f(0, 1, 0)
        for (px, py) in pts:
            glVertex2f(px, py)
        glEnd()

        # líneas
        glBegin(GL_LINES)
        glColor3f(0, 0, 1)
        for a, b in HAND_CONNECTIONS:
            glVertex2f(pts[a][0], pts[a][1])
            glVertex2f(pts[b][0], pts[b][1])
        movement(pts,w)
        glEnd()
    glEnable(GL_DEPTH_TEST)

    # Restaurar matrices
    glPopMatrix()  # MODELVIEW
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def movement(pts, frame_x):
    global zoom, height, angle

    # Mitad de la pantalla en eje X
    screen_mid = frame_x / 2

    # Distancia promedio entre todos los dedos
    dist_prom = (dist(pts[4], pts[8]) + dist(pts[8], pts[12]) + dist(pts[12], pts[16]) + dist(pts[16], pts[20])) / 4
    # Distancia entre la muñeca y el dedo medio
    dist_wrist_middle = dist(pts[0], pts[12])
    # Distancia entre la muñeca y el dedo pequeño
    dist_wrist_pinky = dist(pts[0], pts[20])
    # Distancia entre el dedo índice y el medio
    dist_index_middle = dist(pts[8], pts[12])
    # Distancia entre el dedo medio y la segunda articulación del dedo anular
    dist_middle_ring_dip = dist(pts[12], pts[15])
    # Distancia entre dedo anular y pequeño
    dist_ring_pinky = dist(pts[16], pts[20])
    # Verifica que la señal de movimiento sea correcta: Dedo indice y medio por encima de la mitad de la mano, lejos de los demás dedos
    move_verify = pts[16][0] > pts[9][0] and pts[20][0] > pts[9][0] and dist_middle_ring_dip > 90
    # Verificar solo meñique levantado
    only_pinky = pts[19][1] < pts[14][1] and pts[19][1] < pts[10][1] and pts[19][1] < pts[6][1]
    # Verificar solo indice levantado
    only_index = pts[6][1] < pts[10][1] and pts[6][1] < pts[14][1] and pts[6][1] < pts[19][1]

    # Zoom hacia dentro si todos los dedos están juntos
    if dist_prom < 30.0:
        zoom += 0.005
    # Zoom hacia afuera si todos los dedos están separados y lejos de la muñeca
    if dist_prom > 90 and dist_wrist_middle > 70.0 and dist_wrist_pinky > 70.0 and dist_ring_pinky > 70:
        zoom -= 0.005
    # Habilita movimiento de la escena si el dedo índice y medio están juntos, y el verificador de movimiento es verdadero
    if dist_index_middle < 30.0 and move_verify:
        # Diferencia entre la mitad de la pantalla y la posición del dedo medio para velocidad de rotación
        move_dist = screen_mid - pts[12][0]
        angle += move_dist * 0.001
        # print("Distancia: ", move_dist)
    # Disminuye la altura de la cámara al
    # solo levantar el meñique
    if only_pinky and dist(pts[20],pts[15]) > 40 and dist_prom < 60:
        height -= 0.005
    # Aumenta la altura de la cámara al solo levantar el índice
    if only_index and dist(pts[7],pts[11]) > 30 and 55 < dist_prom < 80:
        height += 0.005

def dist(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )

def ground():
    begin_textured_draw(1)

    glBegin(GL_QUADS)
    glTexCoord2f(0,0);glVertex3f(-15, 0, 15)
    glTexCoord2f(1,0);glVertex3f(-15, 0, -15)
    glTexCoord2f(1,1);glVertex3f(15, 0, -15)
    glTexCoord2f(0,1);glVertex3f(15, 0, 15)
    glEnd()

    end_textured_draw()

def draw_flowers():
    # Considerando que el mapa es 30x30
    # (-15,0,-15) a (15,0,15)

    x_max = 14.5
    z_max = 14

    square_side = 0
    x_offset = -1*x_max
    z_offset = -1*z_max
    flower_angle = 0
    space = 2


    while True:

        glPushMatrix()
        glTranslatef(x_offset, 1.0, z_offset)
        glScalef(2,2,2)
        Flower.draw()
        glPopMatrix()

        if square_side == 0:
            if x_offset < x_max-1: x_offset += space
            else:
                square_side = 1
                z_offset = z_max
                x_offset = x_max+1

        if square_side == 1:
            if x_offset > -1*x_max:  x_offset -= space
            else:
                square_side = 0
                z_offset = -(z_max-1.5)
                x_offset = x_max-0.5
                break

    while True:

        glPushMatrix()
        glTranslatef(x_offset, 1.0, z_offset)
        glRotatef(90,0,1,0)
        glScalef(2, 2, 2)
        Flower.draw()
        glPopMatrix()

        if square_side == 0:
            if z_offset < z_max - 1:
                z_offset += space
            else:
                square_side = 1
                z_offset = z_max+1.5
                x_offset = -x_max+0.25

        if square_side == 1:
            if z_offset > -1 * (z_max-3):
                z_offset -= space
            else:
                break


def draw_damnnnnnnnn():
    global damnn_angle
    damnn_angle += 5

    if damnn_angle >= 360:
        damnn_angle = 0  # Reiniciar el ángulo después de una vuelta completa

    sin_angle = math.sin(math.radians(damnn_angle))
    cos_angle = math.cos(math.radians(damnn_angle))
    scale = 1
    radius = 1.5

    damnn_x = 0.1 *1
    damnn_z = -5.7 *1

    glPushMatrix()
    glTranslatef(damnn_x+radius*cos_angle, 1, damnn_z+radius*sin_angle)
    glRotatef(-damnn_angle, 0, 1, 0)
    glScalef(scale, scale, scale)
    Chingadera.draw()
    glPopMatrix()


def draw_fucking_amazing_fish():
    global ahh_fish_t, ahh_fish_x, ahh_fish_y, ahh_fish_motion, ahh_fish_angle

    if ahh_fish_motion == 1:
        ahh_fish_t -= 0.025 * ahh_fish_motion
        ahh_fish_y = -(ahh_fish_t ** 2) - ahh_fish_t
        ahh_fish_angle = math.degrees(math.atan(-2*ahh_fish_t - 1))
        if ahh_fish_x <= -1:
            ahh_fish_motion *= -1

    if ahh_fish_motion == -1:
        ahh_fish_angle = 0
        ahh_fish_t -= 0.01 * ahh_fish_motion
        ahh_fish_y = -0.1
        if ahh_fish_x >= 0:
            ahh_fish_motion *= -1

    ahh_fish_x = ahh_fish_t

    glPushMatrix()
    glTranslatef(-6.4 - ahh_fish_t, ahh_fish_y, 6.0)
    glRotatef(-ahh_fish_angle,0,0,1)
    normal_fish.draw()
    glPopMatrix()


def draw_floating_crafting_table():
    global floating_table_offset, floating_table_offset, floating_table_motion

    scale =0.25

    floating_table_offset += 0.05 * floating_table_motion

    if floating_table_offset >= 1.25:
        floating_table_motion = -1
    elif floating_table_offset <= 0:
        floating_table_motion = 1

    glPushMatrix()
    glTranslatef(3.8, (17*scale) + floating_table_offset, -8.8)
    glRotatef(damnn_angle, 0 ,1 ,0)
    glScalef(scale, scale, scale)
    normal_crafting.draw()
    glPopMatrix()




def display():
    global angle, minion_t, fish_angle
    global normal_crafting

    normal_crafting = Crafting()

    parametric_square(23)
    minion_jump()
    fish_rotation()


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40, w / h, 0.1, 100.0)


    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(-6.4, 4, 10, # (0, 100, 1) Para vista aérea
              -6.4, 0, 6,
              0, 1, 0)

    # gluLookAt(0, 40, 2,  # (0, 100, 1) Para vista aérea
    #           -0, 0, 0,
    #           0, 1, 0)

    # sin_angle = math.sin(math.radians(fish_angle))
    # cos_angle = math.cos(math.radians(fish_angle))
    # radius = 4
    #
    # gluLookAt(0.0-radius*cos_angle, 10, 2-radius*sin_angle,
    #           0,0,0,
    #           0,1,0)


    # Callback para dibujar las manos
    hands = tracker.get_latest()
    draw_hand_2d(hands)

    glRotatef(angle, 0, 1, 0)

    ground()

    # LIGHT_POLE ##############

    glPushMatrix()
    glTranslatef(-1.8,0,-0.5)
    normal_light_pole.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-8.25, 0, 10)
    normal_light_pole.draw()
    glPopMatrix()

    # ESTANQUE ##########

    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)

    glPushMatrix()
    glColor3f(0.2,0,1)
    glRotatef(90,-1,0,0)
    glTranslatef(4.5,-9,0.01)
    gluDisk(quadric, 0, 1.55, 16, 8)
    glPopMatrix()

    draw_damnnnnnnnn()

    # BUILDING ################

    glPushMatrix()
    glTranslatef(3.1, 0, 3)
    # glRotatef(45,0,0,0)
    normal_building.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(3.8, 0, -8.7)
    # glRotatef(45,0,0,0)
    mini_building.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(8.2, 0, 9.3)
    # glRotatef(45,0,0,0)
    normal_building.draw()
    glPopMatrix()

    # CONGLOMERADO ##
    glPushMatrix()
    glTranslatef(8.75,0,-3.6)
    mini_building.draw()
    glTranslatef(0,0,2.5)
    mini_building.draw()
    glTranslatef(0, 0, 2)
    mini_building.draw()
    glTranslatef(0, 0, 2.5)
    mini_building.draw()
    glPopMatrix()

    # CONGLOMERADO 2 ##
    glPushMatrix()
    glTranslatef(-8.75, 0, -2.5)
    mini_building.draw()
    glTranslatef(0, 0, 1.5)
    mini_building.draw()
    glTranslatef(0, 0, 2)
    mini_building.draw()
    glTranslatef(0, 0, 1.5)
    mini_building.draw()
    glPopMatrix()

    # FLORES
    glPushMatrix()
    draw_flowers()
    glPopMatrix()

    # CRAFTING TABLE
    draw_floating_crafting_table()

    # SOMBRILLAS

    glPushMatrix()
    glTranslatef(-2,0,9.6)
    normal_umbrella.draw((0.753, 0.086, 0.165))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-9.8, -0.2, 9.85)
    glScalef(0.8,0.8, 0.8)
    normal_umbrella.draw((0.305, 0.792, 0.807))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-3.56, -0.4, -0.65)
    glScalef(0.8, 0.8, 0.8)
    normal_umbrella.draw((0.305, 0.807, 0.482))
    glPopMatrix()

    # MINION #####################

    glPushMatrix()
    glTranslatef(-2.2 + (2.2*minion_t_x), minion_t_y*2+.5, 5)
    # glRotatef(45,0,0,0)
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    normal_minion.draw()
    # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glPopMatrix()

    # FISH #######################

    sin_angle = math.sin(math.radians(fish_angle))
    cos_angle = math.cos(math.radians(fish_angle))
    swim = math.sin(math.radians(2*fish_angle))
    radius = 0.25

    # print(f"{sin_angle} and {cos_angle} ")

    # glPushMatrix()
    # glScalef(2,2,2)
    # glRotatef(-90,0,1,0)
    # normal_fish.draw()
    # glPopMatrix()

    glPushMatrix()
    glTranslatef(0+radius*cos_angle, -0.1+(1/8*swim), -6+radius*sin_angle)
    glRotatef(-(fish_angle-270), 0, 1, 0)
    normal_fish.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.4-radius*cos_angle, 0, -6-radius*sin_angle)
    glRotatef(-(fish_angle-90), 0, 1, 0)
    normal_fish.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-6, -0.1+(1/8*sin_angle), 6)
    # glRotatef(-fish_angle, 0, 1, 0)
    normal_fish.draw()
    glPopMatrix()


    glPushMatrix()
    glTranslatef(-5.9+0.5*cos_angle, -0.1+(1/8*swim), 6.0+0.5*sin_angle)
    glRotatef(-(fish_angle-270), 0, 1, 0)
    normal_fish.draw()
    glPopMatrix()

    draw_fucking_amazing_fish()
    # FERRARI ####################

    glPushMatrix()
    glTranslatef(-11 + square_offset_x, 0.0, -11 + square_offset_z)

    if square_t == 90:
        glRotatef(270, 0, 1, 0)
    if square_t == 180:
        glRotatef(-180, 0, 1, 0)
    if square_t == 0:
        glRotatef(0, 0, 1, 0)    # glRotatef(45,0,0,0)
    if square_t == 270:
        glRotatef(90, 0, 1, 0)

    normal_ferrari.draw()
    glPopMatrix()

    # ARBOL ######################

    glPushMatrix()
    glTranslatef(10, -1, 0)
    # glRotatef(45,0,0,0)
    normal_tree.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(2.5, -1, -3.2)
    # glRotatef(45,0,0,0)
    big_tree.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-9.4, -1, -8.2)
    normal_tree.draw()
    glTranslatef(0, 0, -1.5)
    normal_tree.draw()
    glTranslatef(1.5, 0, 0)
    normal_tree.draw()
    glTranslatef(0, 0, 1.5)
    normal_tree.draw()
    glPopMatrix()

    # OXXO ########################

    glPushMatrix()
    glTranslatef(5.5, 1, -8.7)
    normal_oxxo.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-10, 0.5, 8.65)
    mini_oxxo.draw()
    glPopMatrix()

    glPushMatrix()
    glRotatef(90, 0, -1, 0)
    glTranslatef(-3.5, 0.5, 2.75)
    mini_oxxo.draw()
    glTranslatef(3.7,0,0)
    mini_oxxo.draw()
    glPopMatrix()

    glutSwapBuffers()

    glutKeyboardFunc(keyboard)

def idle():
    global angle
    glutPostRedisplay()
    #angle += 0.001

# Terminar proceso con 'q' o ESC
def keyboard(key):
    if key in [b'q', b'\x1b']:  # '\x1b' = ESC
        sys.exit(0)

def main():
    global tracker
    from Util.Landmarks import LandmarksTracker  # si lo separas en archivo

    pygame.mixer.init()

    tracker = LandmarksTracker(MODEL_PATH)
    tracker.start()

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(w, h)
    glutCreateWindow(b"Ciudad P. Luche")

    load_texture("Street/vista-superior-arriba-es-mapa-calles-manzana_70347-4067.jpg")
    pygame.mixer.music.load(
        "funkytown.mp3")

    init()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    pygame.mixer.music.play()
    glutMainLoop()


if __name__ == "__main__":
    main()
