from OpenGL.GL import *
from OpenGL.GLU import *


def begin_solid_draw():
    glPushAttrib(
        GL_CURRENT_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT | GL_TEXTURE_BIT | GL_LINE_BIT )

def end_solid_draw():
    glPopAttrib()


def draw_line(p1, p2, color=(1, 0, 0), width=2.0):
    begin_solid_draw()

    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glLineWidth(width)
    glColor3f(*color)

    glBegin(GL_LINES)
    glVertex3f(*p1)
    glVertex3f(*p2)
    glEnd()

    end_solid_draw()

def draw_cone(x, y, z, base_radius, height, color=(1, 0, 0)):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(0, 0, 0, 1)
    glRotatef(-90, 1, 0, 0)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluCylinder(quad, base_radius, 0, height, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()


def draw_umbrella(umbrella_color=(1,1,1)):
    draw_cone(0, 1.25, 0.15, 0.65, 0.25, umbrella_color)

    draw_line((0,1.25,0.15),(0,0,0.15), (0.69,.69,.69), 10 )


class Umbrella:
    @staticmethod
    def draw(color=(1,1,1)):
        glPushMatrix()
        draw_umbrella(color)
        glPopMatrix()