from OpenGL.GL import *

class Building:
    def __init__(self, size=1.0):
        self.s = size

    def draw(self):
        s = self.s
        b0 = (-s, 0, s)
        b1 = (-s, 0, -s)
        b2 = (s, 0, -s)
        b3 = (s, 0, s)

        # BASE
        # b1 == b2
        # ||    ||
        # b0 == b3

        glBegin(GL_QUADS)

        # Base
        glColor3f(0,0,0)
        glVertex3f(*b0)
        glVertex3f(*b1)
        glVertex3f(*b2)
        glVertex3f(*b3)

        glColor3f(0.5, 0.5, 0.5)

        # Pared izquierda
        glVertex3f(*b0)
        glVertex3f(*b1)
        glVertex3f(*suma(b1,(0,int(s * 4),0)))
        glVertex3f(*suma(b0,(0,int(s * 4),0)))

        # Pared frontal
        glVertex3f(*b1)
        glVertex3f(*b2)
        glVertex3f(*suma(b2, (0, int(s * 4), 0)))
        glVertex3f(*suma(b1, (0, int(s * 4), 0)))

        # Pared derecha
        glVertex3f(*b2)
        glVertex3f(*b3)
        glVertex3f(*suma(b3, (0, int(s * 4), 0)))
        glVertex3f(*suma(b2, (0, int(s * 4), 0)))

        # Pared trasera
        glVertex3f(*b0)
        glVertex3f(*b3)
        glVertex3f(*suma(b3, (0, int(s * 4), 0)))
        glVertex3f(*suma(b0, (0, int(s * 4), 0)))

        glColor3f(1, 1, 1)

        # Techo
        glVertex3f(*suma(b0, (0, int(s * 4), 0)))
        glVertex3f(*suma(b1, (0, int(s * 4), 0)))
        glVertex3f(*suma(b2, (0, int(s * 4), 0)))
        glVertex3f(*suma(b3, (0, int(s * 4), 0)))

        glEnd()

def suma(t1,t2):
    return tuple(map(sum, zip(t1, t2)))

