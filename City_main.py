import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Alive.Minion import Minion
from Street.building import Building
from Street.light_pole import LightPole
from Util.Landmarks import HAND_CONNECTIONS

# Modelo para landmarks
MODEL_PATH = r"C:\Users\monte\Downloads\hand_landmarker.task"

w, h = 800, 600
# Ángulo de rotación inicial
angle = 0.0
# Zoom inicial
zoom = 4
# Declaración del rastreador de landmarks
tracker = None

b1 = Building(1.5)
m1 = Minion(0.5)
lp1 = LightPole(1)

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)


def reshape(width, height):
    global w, h
    w, h = width, max(height, 1)
    glViewport(0, 0, w, h)

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
    global zoom, angle

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

    # Zoom hacia dentro si todos los dedos están juntos
    if dist_prom < 30.0:
        zoom += 0.001
    # Zoom hacia afuera si todos los dedos están separados y lejos de la muñeca
    if dist_prom > 90 and dist_wrist_middle > 70.0 and dist_wrist_pinky > 70.0 and dist_ring_pinky > 70:
        zoom -= 0.001
    # Habilita movimiento de la escena si el dedo índice y medio están juntos, y el verificador de movimiento es verdadero
    if dist_index_middle < 30.0 and move_verify:
        # Diferencia entre la mitad de la pantalla y la posición del dedo medio para velocidad de rotación
        move_dist = screen_mid - pts[12][0]
        angle += move_dist * 0.0001
        print("Distancia: ", move_dist)


def dist(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )

def ground():
    glColor3f(0,0.7,0)
    glBegin(GL_QUADS)
    glVertex3f(-15, 0, 15)
    glVertex3f(-15, 0, -15)
    glVertex3f(15, 0, -15)
    glVertex3f(15, 0, 15)
    glEnd()

def display():
    global angle, zoom

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40, w / h, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 6, zoom, # (0, 100, 1) Para vista aérea
              0, 0, 0,
              0, 1, 0
    )

    # Callback para dibujar las manos
    hands = tracker.get_latest()
    draw_hand_2d(hands)

    ground()

    glRotatef(angle, 0, 1, 0)

    glPushMatrix()
    glTranslatef(0,0,0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    lp1.draw()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(3, 0, 2)
    # glRotatef(45,0,0,0)
    b1.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-3, 0, 2)
    # glRotatef(45,0,0,0)
    m1.draw()
    glPopMatrix()

    glutSwapBuffers()

def idle():
    global angle
    glutPostRedisplay()
    angle += 0.0007


def main():
    global tracker
    from Util.Landmarks import LandmarksTracker  # si lo separas en archivo

    tracker = LandmarksTracker(MODEL_PATH)
    tracker.start()

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(w, h)
    glutCreateWindow(b"Ciudad P. Luche")

    init()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMainLoop()


if __name__ == "__main__":
    main()
