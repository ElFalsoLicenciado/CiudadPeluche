from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GLU import *


class Minion:
    def __init__(self, size=1):
        self.s = size

    def draw(self):
        s = self.s

        quad = gluNewQuadric()

        glColor3f(1,1,0)

        glPushMatrix()
        glRotatef(90,-1,0,0)
        gluCylinder(quad, s/2, s/2, s, 16, 1)
        glPopMatrix()

        glTranslatef(0, s,0)
        gluSphere(quad, s / 2, 16, 16)
        glTranslatef(0, -s, 0)
        gluSphere(quad, s / 2, 16, 16)