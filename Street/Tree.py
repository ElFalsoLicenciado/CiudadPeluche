from OpenGL.GL import *
from OpenGL.raw.GLU import *
from OpenGL.raw.GLUT import *

quadric = None

class Tree:
    def __init__(self, size=1):
        self.s = size
        global quadric

        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)

    def draw(self):
        s = self.s

        global quadric

        # Ajustes low-poly
        trunk_h = 1.1 * s
        trunk_r = 0.14 * s
        crown_h1 = 1.0 * s
        crown_h2 = 0.85 * s
        crown_h3 = 0.70 * s
        crown_r1 = 0.75 * s
        crown_r2 = 0.60 * s
        crown_r3 = 0.48 * s

        trunk_slices = 6    # pocos lados = low-poly real
        crown_slices = 7    # conos faceteados

        glPushMatrix()

        # Para que se vea facetado (sin suavizado excesivo)
        glShadeModel(GL_FLAT)

        # --- Tronco (cilindro low-poly) ---
        glColor3f(0.4, 0.35, 0.2)
        glPushMatrix()
        glTranslatef(0, trunk_h * 0.5, 0)
        glRotatef(-90, 1, 0, 0)  # cilindro a lo largo de +Y
        gluCylinder(quadric, trunk_r, trunk_r * 0.9, trunk_h, trunk_slices, 1)
        glPopMatrix()

        # --- Copas (conos apilados) ---
        glColor3f(0, 0.4, 0)

        # Cono 1 (abajo)
        glPushMatrix()
        glTranslatef(0, trunk_h + 0.15 * s, 0)
        glRotatef(-90, 1, 0, 0)
        glutSolidCone(crown_r1, crown_h1, crown_slices, 1)
        glPopMatrix()

        # Cono 2 (medio)
        glPushMatrix()
        glTranslatef(0, trunk_h + 0.55 * s, 0)
        glRotatef(-90, 1, 0, 0)
        glutSolidCone(crown_r2, crown_h2, crown_slices, 1)
        glPopMatrix()

        # Cono 3 (arriba)
        glPushMatrix()
        glTranslatef(0, trunk_h + 0.90 * s, 0)
        glRotatef(-90, 1, 0, 0)
        glutSolidCone(crown_r3, crown_h3, crown_slices, 1)
        glPopMatrix()

        # Regresa a suave si tu escena lo usa
        glShadeModel(GL_SMOOTH)

        glPopMatrix()