from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GLU import *


class LightPole:
    def __init__(self, size=1.0):
        self.s = size

    def draw(self):
        s = self.s

        quad = gluNewQuadric()

        glColor3f(0.1, 0.1, 0.1)

        # Base
        glPushMatrix()
        glRotatef(90, -1, 0, 0)
        gluCylinder(quad, s / 4, 0, s/4, 8, 1)
        glPopMatrix()

        # Cuerpo
        glPushMatrix()
        glRotatef(90, -1, 0, 0)
        glTranslatef(0, 0,s/8)
        gluCylinder(quad, s / 8, s/8, 3, 16, 1)
        glPopMatrix()

        # Brazo

        # LED

