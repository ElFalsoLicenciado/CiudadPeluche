from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Alive.Fish import Fish
from Alive.Ferrari import Ferrari
from Street.Arbol import Arbol
from Street.building import Building

angle = 0.0

f1 = Fish(0.5)
ferr = Ferrari()
a1 = Arbol()
b1 = Building()

w, h = 800, 600

def init_gl():
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)

def reshape(width, height):
    global w, h
    w, h = width, max(height, 1)
    glViewport(0, 0, w, h)

def display():
    global angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40, w / h, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 4, 7,  # (0, 100, 1) Para vista aérea
              0, 0, 0,
              0, 1, 0
              )

    glRotate(angle, 0.3, 1, 0)

    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glTranslatef(0, 0, 0)
    f1.draw()
    #glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glutSwapBuffers()

    glutKeyboardFunc(keyboard)

    angle += 0.02

def idle():
    glutPostRedisplay()

def keyboard(key):
    if key in [b'q', b'\x1b']:  # '\x1b' = ESC
        sys.exit(0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(w, h)
    glutCreateWindow(b"Testing Field")

    init_gl()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
