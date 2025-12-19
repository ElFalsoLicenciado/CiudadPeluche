from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GLU import *


def pyramid(sz):
    apex = (0, sz, 0)  # punta
    v0 = (-sz, -sz, sz)  # base
    v1 = (sz, -sz, sz)
    v2 = (sz, -sz, -sz)
    v3 = (-sz, -sz, -sz)

    # Caras laterales (triángulos)
    glBegin(GL_TRIANGLES)

    glColor3f(1, 0, 0)  # frente
    glVertex3f(*apex)
    glVertex3f(*v0)
    glVertex3f(*v1)

    glColor3f(0, 1, 0)  # derecha
    glVertex3f(*apex)
    glVertex3f(*v1)
    glVertex3f(*v2)

    glColor3f(0, 0, 1)  # atrás
    glVertex3f(*apex)
    glVertex3f(*v2)
    glVertex3f(*v3)

    glColor3f(1, 1, 0)  # izquierda
    glVertex3f(*apex)
    glVertex3f(*v3)
    glVertex3f(*v0)

    glEnd()

    # Base (cuadrado)
    glBegin(GL_QUADS)
    glColor3f(0, 0, 0.75)
    glVertex3f(*v0)
    glVertex3f(*v1)
    glVertex3f(*v2)
    glVertex3f(*v3)
    glEnd()


class Fish:
    def __init__(self, size=1):
        self.s = size

    def draw(self):
        s = self.s

        quad = gluNewQuadric()

        glColor3f(0,0,0.75)

        glPushMatrix()
        glRotatef(90, 0, -1, 0)
        gluCylinder(quad, s, s/2, s*2, 32, 1)
        glPopMatrix()

        quad = gluNewQuadric()

        glPushMatrix()
        gluSphere(quad, s, 16, 16)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-s*1.9, 0, 0)
        glRotatef(90, 0, 0, -1)
        pyramid(s*0.75)
        glPopMatrix()

        glPushMatrix()

        glPopMatrix()