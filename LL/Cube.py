from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

w, h = 800, 600
angle = 0.0

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)

def reshape(width, height):
    global w, h
    w, h = width, max(height, 1)
    glViewport(0, 0, w, h)

# TODO para dibujar un cubo en la escena
def draw_cube():
    # Cubo de lado 2 (de -1 a 1)
    glBegin(GL_QUADS)

    # Frente (z = +1)
    glColor3f(1, 0, 0)
    glVertex3f(-1, -1,  1)
    glVertex3f( 1, -1,  1)
    glVertex3f( 1,  1,  1)
    glVertex3f(-1,  1,  1)

    # Atrás (z = -1)
    glColor3f(0, 1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1,  1, -1)
    glVertex3f( 1,  1, -1)
    glVertex3f( 1, -1, -1)

    # Izquierda (x = -1)
    glColor3f(0, 0, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1,  1)
    glVertex3f(-1,  1,  1)
    glVertex3f(-1,  1, -1)

    # Derecha (x = +1)
    glColor3f(1, 1, 0)
    glVertex3f( 1, -1, -1)
    glVertex3f( 1,  1, -1)
    glVertex3f( 1,  1,  1)
    glVertex3f( 1, -1,  1)

    # Arriba (y = +1)
    glColor3f(0, 1, 1)
    glVertex3f(-1,  1, -1)
    glVertex3f(-1,  1,  1)
    glVertex3f( 1,  1,  1)
    glVertex3f( 1,  1, -1)

    # Abajo (y = -1)
    glColor3f(1, 0, 1)
    glVertex3f(-1, -1, -1)
    glVertex3f( 1, -1, -1)
    glVertex3f( 1, -1,  1)
    glVertex3f(-1, -1,  1)

    glColor3f(1, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(2, 0, 0)
    glVertex3f(2, 0, 2)
    glVertex3f(0, 0, 2)

    glEnd()

def display():
    global angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, w / h, 0.1, 100.0)

    # MODELVIEW (cámara + mundo)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        2, 4, 6,   # cámara más lejos para ver el cubo
        0, 0, 0,   # mira al origen
        0, 1, 0    # arriba
    )

    # Rotación 3D (Y y un poquito en X para que se vea volumétrico)
    glRotatef(angle, 0, 1, 0)
    glRotatef(angle * 0.6, 1, 0, 0)

    draw_cube()

    glutSwapBuffers()
    angle += 1.5

def idle():
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(w, h)
    glutCreateWindow(b"Cubo 3D Rotando")

    init()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
