import math
from OpenGL.GL import *
from OpenGL.GLU import *


def begin_solid_draw():
    glPushAttrib(
        GL_CURRENT_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT | GL_TEXTURE_BIT | GL_LINE_BIT )


def end_solid_draw():
    glPopAttrib()

def draw_sphere(x, y, z, radius, color=(1, 1, 1)):
    begin_solid_draw()

    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glColor3f(*color)

    glPushMatrix()
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, radius, 20, 20)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    end_solid_draw()


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


def draw_chingadera():

    angle = math.sin(math.radians(30))

    color_patas = (0.776, 0.616, 0.529)
    color_cuerpo = (0.208, 0.157, 0.161)
    color_pico = (0.239, 0.231, 0.227)

    pata_x = 0.075

    eye_x = 0.07
    eye_y = 1.12
    eye_z = 0.24
    eye_size = 0.03


    # Pata izquierda
    draw_line((-pata_x, 0.1, 0), (-pata_x, 1, 0), color_patas, 3.0 )
    draw_line((-pata_x, 0.1, 0), (-pata_x+(-pata_x*angle), 0.1, 0+(0.5*angle)), color_patas, 2.5 )
    draw_line((-pata_x, 0.1, 0), (-pata_x, 0.1, 0.5*angle), color_patas, 2.5 )
    draw_line((-pata_x, 0.1, 0), (-pata_x-(-pata_x*angle), 0.1, 0+(0.5*angle)), color_patas, 2.5 )


    # Pata derecha
    draw_line((pata_x, 0.1, 0), (pata_x, 1, 0), color_patas, 3.0 )
    draw_line((pata_x, 0.1, 0), (pata_x+(pata_x*angle), 0.1, 0+(0.5*angle)), color_patas, 2.5 )
    draw_line((pata_x, 0.1, 0), (pata_x, 0.1, 0.5*angle), color_patas, 2.5 )
    draw_line((pata_x, 0.1, 0), (pata_x-(pata_x*angle), 0.1, 0+(0.5*angle)), color_patas, 2.5 )

    # Cuerpo,
    glPushMatrix()
    glScalef(1, 1, 1.5)
    draw_sphere(0, 1, 0, 0.15, color_cuerpo)
    glPopMatrix()

    # Cabeza
    glPushMatrix()
    glScalef(1, 1, 1.25)
    draw_sphere(0, 1.10, 0.15, 0.1, color_cuerpo)
    glPopMatrix()

    # Pico
    glPushMatrix()
    glTranslatef(0, 1.25, -1.05)
    glRotatef(90, 1, 0, 0)
    draw_cone(0, 1.25, 0.15, 0.05, 0.3, color_pico)
    glPopMatrix()

    # Ojos

    glPushMatrix()
    glTranslatef(eye_x, eye_y, eye_z)
    draw_sphere(0, 0, 0, eye_size, (0,0,0))
    glPopMatrix()
    glPushMatrix()
    glTranslatef(eye_x * -1, eye_y, eye_z)
    draw_sphere(0, 0, 0, eye_size, (0,0,0))
    glPopMatrix()

class Chingadera:
    @staticmethod
    def draw():
        glPushMatrix()
        draw_chingadera()
        glPopMatrix()