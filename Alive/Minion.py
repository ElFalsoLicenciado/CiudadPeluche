from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GLU import *


class Minion:
    def __init__(self, size=1):
        self.s = size

    def draw(self):
        s = self.s
        quad = gluNewQuadric()

        glColor3f(1, 1, 0)

        glPushMatrix()
        glTranslatef(0, -s / 2, 0)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, s / 2, s / 2, s, 16, 1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, s / 2, 0)
        gluSphere(quad, s / 2, 16, 16)
        glPopMatrix()

        glColor3f(0, 0.333, 0.878)
        glPushMatrix()
        glTranslatef(0, -s / 2, 0)
        gluSphere(quad, s / 2, 16, 16)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, s/3, s/2 + 0.01)

        glColor3f(1, 1, 1)
        gluSphere(quad, s/4, 16, 16)

        glTranslatef(0, 0, s/6)
        glColor3f(0, 0, 0)
        gluSphere(quad, s/10, 16, 16)

        glPopMatrix()

        glColor3f(0.1, 0.1, 0.1)
        glPushMatrix()
        glTranslatef(0, s/3, 0)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, s/1.75, s/2.01, s/6, 16, 1)
        glPopMatrix()

        glColor3f(1, 1, 0)

        for side in [-1, 1]:
            glPushMatrix()
            glTranslatef(side * s/2.3, -s*.25, 0)
            glRotatef(90, 0, 0, 1)
            gluCylinder(quad, s/10, s/10, s*0.75, 8, 1)
            glPopMatrix()

        glColor3f(0, 0, 0)

        for side in [-0.2, 0.2]:
            glPushMatrix()
            glTranslatef(side * s, -s, s/9)
            glScalef(1,1,1.75)
            gluSphere(quad, s/6, 8, 8)
            glPopMatrix()

        glColor3f(0, 0.333, 0.878)
        glPushMatrix()
        glTranslatef(0, -s / 2, 0)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, s / 1.99, s / 1.99, s/2.2, 16, 1)
        glPopMatrix()
