from OpenGL.GL import *

def draw_rect_1(s, color):
    b0 = (-s, 0, s)
    b1 = (-s, 0, -s)
    b2 = (s, 0, -s)
    b3 = (s, 0, s)

    # BASE
    # b1 == b2
    # ||    ||
    # b0 == b3

    glBegin(GL_QUADS)

    glColor3f(*color)

    # Base
    glVertex3f(*b0)
    glVertex3f(*b1)
    glVertex3f(*b2)
    glVertex3f(*b3)

    # Pared izquierda
    glVertex3f(*b0)
    glVertex3f(*b1)
    glVertex3f(*suma(b1, (0, int(s * 4), 0)))
    glVertex3f(*suma(b0, (0, int(s * 4), 0)))

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

    # Techo
    glVertex3f(*suma(b0, (0, int(s * 4), 0)))
    glVertex3f(*suma(b1, (0, int(s * 4), 0)))
    glVertex3f(*suma(b2, (0, int(s * 4), 0)))
    glVertex3f(*suma(b3, (0, int(s * 4), 0)))

    glEnd()

def draw_rect_2(s,color):
    b0 = (-s/2, 0, s)
    b1 = (-s/2, 0, -s)
    b2 = (s/2, 0, -s)
    b3 = (s/2, 0, s)

    # BASE
    # b1 == b2
    # ||    ||
    # b0 == b3

    glBegin(GL_QUADS)

    glColor3f(*color)

    # Base
    glVertex3f(*b0)
    glVertex3f(*b1)
    glVertex3f(*b2)
    glVertex3f(*b3)

    # Pared izquierda
    glVertex3f(*b0)
    glVertex3f(*b1)
    glVertex3f(*suma(b1, (0, int(s * 4), 0)))
    glVertex3f(*suma(b0, (0, int(s * 4), 0)))

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

    # Techo
    glVertex3f(*suma(b0, (0, int(s * 4), 0)))
    glVertex3f(*suma(b1, (0, int(s * 4), 0)))
    glVertex3f(*suma(b2, (0, int(s * 4), 0)))
    glVertex3f(*suma(b3, (0, int(s * 4), 0)))

    glEnd()

def suma(t1,t2):
    return tuple(map(sum, zip(t1, t2)))


class Oxxo:
    def __init__(self, size=1):
        self.size = size

    def draw(self):
        s = self.size

        glPushMatrix()
        glRotate(90, 0, 0, -1)
        draw_rect_1(s, (255, 255, 0))
        glPopMatrix()

        glPushMatrix()
        glRotate(90, 0, 0, -1)
        glTranslate(-s, -s/2, 0)
        draw_rect_2(s * 1.25, (255, 0, 0))
        glPopMatrix()

        glPushMatrix()
        glColor3f(0, 0, 0)
        glTranslatef(s * 1.3, -s/2, s + 0.01)
        glBegin(GL_QUADS)
        glVertex2f(-s/2, -s/2)
        glVertex2f(-s/2, s/2)
        glVertex2f(s, s/2)
        glVertex2f(s, -s/2)
        glEnd()
        glPopMatrix()