from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

w, h = 800, 600

# TODO. Se agrega una nueva variable global, la cual se usará para el valor de rotación inicial y mantener cambios durante la ejecución
angle = 0.0

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
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
    gluPerspective(60.0, w / h, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 3,
              0, 0, 0,
              0, 1, 0)

# TODO mismo código. se agrega esta función, la cual hará la matriz a la que se aplique (al objeto en la escena en este caso), mientras la camará sigue en su lugar
    glRotatef(angle, 0, 1, 0)

    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0); glVertex3f(-1, -1, 0)
    glColor3f(0, 1, 0); glVertex3f( 1, -1, 0)
    glColor3f(0, 0, 1); glVertex3f( 0,  1, 0)
    glEnd()

    glutSwapBuffers()

# TODO. Se aumenta el ángulo de rotación de la escena en 'angle' grados
    angle += 0.5  # velocidad de rotación

def idle():
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(w, h)
    glutCreateWindow(b"OpenGL Rotando")

    init()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
