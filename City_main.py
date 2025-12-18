from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Alive.Minion import Minion
from Street.building import Building
from Street.light_pole import LightPole

w, h = 800, 600
angle = 0.0
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

def ground():
    glColor3f(0,0.7,0)
    glBegin(GL_QUADS)
    glVertex3f(-15, 0, 15)
    glVertex3f(-15, 0, -15)
    glVertex3f(15, 0, -15)
    glVertex3f(15, 0, 15)
    glEnd()

def display():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40, w / h, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 6, 4, # (0, 100, 1) Para vista aérea
              0, 3, 0,
              0, 1, 0
    )

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
    angle += 0.1


def idle():
    glutPostRedisplay()


def main():
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
