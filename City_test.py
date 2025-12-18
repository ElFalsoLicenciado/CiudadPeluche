from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Util.Landmarks import HAND_CONNECTIONS

MODEL_PATH = r"C:\Users\monte\Downloads\hand_landmarker.task"

w, h = 800, 600
tracker = None

def init_gl():
    glClearColor(0, 0, 0, 1)

def reshape(width, height):
    global w, h
    w, h = width, max(height, 1)
    glViewport(0, 0, w, h)

def draw_hand_2d(hands):
    # Dibujar en coordenadas de pantalla (0..w, 0..h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, h, 0)  # ojo: y hacia abajo para parecerse a OpenCV

    glMatrixMode(GL_MODELVIEW)
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
        glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    hands = tracker.get_latest()
    draw_hand_2d(hands)

    glutSwapBuffers()

def idle():
    glutPostRedisplay()

def main():
    global tracker
    from Util.Landmarks import LandmarksTracker  # si lo separas en archivo

    tracker = LandmarksTracker(MODEL_PATH)
    tracker.start()

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(w, h)
    glutCreateWindow(b"OpenGL + MediaPipe")

    init_gl()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
