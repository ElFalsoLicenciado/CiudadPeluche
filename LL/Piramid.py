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

def draw_pyramid():
    # Vértices
    apex = (0, 1, 0)       # punta
    v0 = (-1, -1,  1)      # base
    v1 = ( 1, -1,  1)
    v2 = ( 1, -1, -1)
    v3 = (-1, -1, -1)

    # Caras laterales (triángulos)
    glBegin(GL_TRIANGLES)

    glColor3f(1, 0, 0)  # frente
    glVertex3f(*apex); glVertex3f(*v0); glVertex3f(*v1)

    glColor3f(0, 1, 0)  # derecha
    glVertex3f(*apex); glVertex3f(*v1); glVertex3f(*v2)

    glColor3f(0, 0, 1)  # atrás
    glVertex3f(*apex); glVertex3f(*v2); glVertex3f(*v3)

    glColor3f(1, 1, 0)  # izquierda
    glVertex3f(*apex); glVertex3f(*v3); glVertex3f(*v0)
    
    glEnd()

    # Base (cuadrado)
    glBegin(GL_QUADS)
    glColor3f(0.7, 0.7, 0.7)
    glVertex3f(*v0); glVertex3f(*v1); glVertex3f(*v2); glVertex3f(*v3)
    glEnd()

def display():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, w / h, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 6,  0, 0, 0,  0, 1, 0)

    glRotatef(angle, 0, 1, 0)
    glRotatef(angle * 0.6, 1, 0, 0)

    draw_pyramid()

    glutSwapBuffers()
    angle += 0.8

def idle():
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(w, h)
    glutCreateWindow(b"Piramide 3D")

    init()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
