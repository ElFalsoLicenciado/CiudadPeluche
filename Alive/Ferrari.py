from OpenGL.GL import *
from OpenGL.raw.GLU import *
from OpenGL.raw.GLUT import *

quadric = gluNewQuadric()

def draw_box(sx, sy, sz):
    glPushMatrix()
    glScalef(sx, sy, sz)
    glutSolidCube(1.0)
    glPopMatrix()

def draw_wheel(radius, width, s):
    global quadric

    glPushMatrix()
    glRotatef(90, 0, 0, 1)  # alinear cilindro al eje X
    glTranslatef(s * 0.3, 0, s * -0.2)

    # Neumático
    glColor3f(0.2, 0.2, 0.2)
    gluCylinder(quadric, radius, radius, width, 28, 1)

    # Tapas neumático
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    gluDisk(quadric, 0.0, radius, 28, 1)
    glTranslatef(0, 0, width)
    gluDisk(quadric, 0.0, radius, 28, 1)
    glPopMatrix()

    # Rin
    glColor3f(0.7, 0,0)
    glTranslatef(0, 0, s * -0.02)
    gluCylinder(quadric, radius * 0.65, radius * 0.65, width * 1.2, 28, 1)

    # Centro rin
    glTranslatef(0, 0, s * -0.02)
    gluCylinder(quadric, radius * 0.5, radius * 0.5, width * 1.2, 24, 1)

    #Tapas rin
    glTranslatef(0, 0, s * 0.22)
    gluSphere(quadric, radius * 0.6, 16, 16)

    glPopMatrix()

def draw_car(s):
    # Proporciones del carro
    bodyL = s * 4.2
    bodyW = s * 1.85
    bodyH = s * 0.55

    wheelR = s * 0.42
    wheelW = s * 0.35

    # Carrocería
    glColor3f(1,0,0)
    glPushMatrix()
    glTranslatef(0, wheelR + bodyH * 0.5, 0)
    draw_box(bodyL, bodyH, bodyW)
    glPopMatrix()

    # Cofre inclinado
    glPushMatrix()
    glTranslatef(+bodyL * 0.22, wheelR + bodyH * 0.65, 0)
    glRotatef(-12, 0, 0, 1)
    draw_box(bodyL * 0.55, bodyH * 0.35, bodyW * 0.92)
    glPopMatrix()

    # Alerón trasero
    glColor3f(0,0,0)
    glPushMatrix()
    glTranslatef(-bodyL * 0.42, wheelR + bodyH * 1.05, 0)
    draw_box(bodyL * 0.18, bodyH * 0.10, bodyW * 0.75)
    glPopMatrix()

    # Cabina
    glColor3f(0,0,0.7)
    glPushMatrix()
    glTranslatef(-bodyL * 0.05, wheelR + bodyH * 1.05, 0)
    glScalef(bodyL * 0.45, bodyH * 0.85, bodyW * 0.75)
    glutSolidSphere(0.55, 26, 18)
    glPopMatrix()

    # Splitter frontal
    glColor3f(0,0,0)
    glPushMatrix()
    glTranslatef(+bodyL * 0.52, wheelR + bodyH * 0.18, 0)
    draw_box(bodyL * 0.08, bodyH * 0.10, bodyW * 0.95)
    glPopMatrix()

    # Faros
    glColor3f(1,1,0)
    glPushMatrix()
    glTranslatef(+bodyL * 0.50, wheelR + bodyH * 0.55, +bodyW * 0.32)
    glutSolidSphere(s * 0.08, 16, 12)
    glTranslatef(0, 0, -bodyW * 0.64)
    glutSolidSphere(s * 0.08, 16, 12)
    glPopMatrix()

    # Ruedas (4)
    # delanteras
    glPushMatrix()
    glTranslatef(+bodyL * 0.28, 0, +bodyW * 0.52)
    draw_wheel(wheelR, wheelW, s)
    glTranslatef(0, 0, -bodyW * 1.04)
    draw_wheel(wheelR, wheelW, s)
    glPopMatrix()

    # traseras (+ grandes)
    glPushMatrix()
    glTranslatef(-bodyL * 0.30, 0, +bodyW * 0.52)
    draw_wheel(wheelR * 1.05, wheelW * 1.05, s)
    glTranslatef(0, 0, -bodyW * 1.04)
    draw_wheel(wheelR * 1.05, wheelW * 1.05, s)
    glPopMatrix()

class Ferrari:
    def __init__(self, size=1):
        self.s = size
        global quadric

        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)

    def draw(self):
        s = self.s

        glPushMatrix()
        glTranslatef(0, 0.02, 0)  # leve levantada
        draw_car(s)
        glPopMatrix()