from OpenGL.GL import *
from PIL import Image

tex_craft_top = None
tex_craft_bottom = None
tex_craft_side = None
tex_craft_front = None



def begin_solid_draw():
    glPushAttrib(
        GL_CURRENT_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT | GL_TEXTURE_BIT | GL_LINE_BIT )


def end_solid_draw():
    glPopAttrib()


def texture(path):
    img = Image.open(path)
    img = img.transpose(Image.ROTATE_180)  # OpenGL usa origen abajo
    img_data = img.convert("RGBA").tobytes()

    width, tex_height = img.size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA,
        width, tex_height, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, img_data
    )

    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id

    # img = Image.open(path)
    # img = img.transpose(Image.ROTATE_180)  # OpenGL usa origen abajo
    # img_data = img.convert("RGBA").tobytes()
    #
    # tex_id = glGenTextures(1)
    # glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    #
    # glBindTexture(GL_TEXTURE_2D, tex_id)
    #
    # # Filtrado
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    #
    # # Envoltura (tiling)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    #
    # # Subir la textura
    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
    #              img.width, img.height, 0,
    #              GL_RGB, GL_UNSIGNED_BYTE, img_data)
    #
    # # Crear mipmaps
    # glGenerateMipmap(GL_TEXTURE_2D)
    #
    # glBindTexture(GL_TEXTURE_2D, 0)
    #
    # return tex_id


def draw_textured_cube(texture_top=None, texture_bottom=None, texture_side=None, texture_front=None):
    begin_solid_draw()

    glBindTexture(GL_TEXTURE_2D, texture_front)

    glBegin(GL_QUADS)

    # Frente (z = +1)
    glColor3f(1, 1, 1)
    glTexCoord2f(0, 0); glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 0); glVertex3f(1, -1, 1)
    glTexCoord2f(1, 1); glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1, 1)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)

    glBindTexture(GL_TEXTURE_2D, texture_front)
    glBegin(GL_QUADS)
    # Atrás (z = -1)
    glColor3f(1, 1, 1)

    glTexCoord2f(0, 0); glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0); glVertex3f(-1, 1, -1)
    glTexCoord2f(1, 1); glVertex3f(1, 1, -1)
    glTexCoord2f(0, 1); glVertex3f(1, -1, -1)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)

    glBindTexture(GL_TEXTURE_2D, texture_side)
    glBegin(GL_QUADS)
    # Izquierda (x = -1)
    glColor3f(1, 1, 1)
    glTexCoord2f(0, 0); glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0); glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 1); glVertex3f(-1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1, -1)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)

    glBindTexture(GL_TEXTURE_2D, texture_side)
    glBegin(GL_QUADS)
    # Derecha (x = +1)
    glColor3f(1, 1, 1)
    glTexCoord2f(0, 0); glVertex3f(1, -1, -1)
    glTexCoord2f(1, 0); glVertex3f(1, -1, 1)
    glTexCoord2f(1, 1); glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(1, 1, -1)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)

    glBindTexture(GL_TEXTURE_2D, texture_top)
    glBegin(GL_QUADS)
    # Arriba (y = +1)
    glColor3f(1, 1, 1)
    glTexCoord2f(0, 0); glVertex3f(-1, 1, -1)
    glTexCoord2f(1, 0); glVertex3f(-1, 1, 1)
    glTexCoord2f(1, 1); glVertex3f(1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(1, 1, -1)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)

    glBindTexture(GL_TEXTURE_2D, texture_bottom)
    glBegin(GL_QUADS)
    # Abajo (y = -1)
    glColor3f(1, 1, 1)
    glTexCoord2f(0, 0); glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0); glVertex3f(1, -1, -1)
    glTexCoord2f(1, 1); glVertex3f(1, -1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, -1, 1)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)

    end_solid_draw()

class Crafting:
    def __init__(self):
        global tex_craft_top, tex_craft_bottom, tex_craft_side, tex_craft_front
        self.tex_craft_top = texture("Street/crafting_top.png")
        self.tex_craft_bottom = texture("Street/oak_planks.png")
        self.tex_craft_side = texture("Street/crafting_side.png")
        self.tex_craft_front = texture("Street/crafting_front.png")

    def draw(self):
        top = self.tex_craft_top
        bottom = self.tex_craft_bottom
        side = self.tex_craft_side
        front = self.tex_craft_front

        glPushMatrix()
        draw_textured_cube(top, bottom, side, front)
        glPopMatrix()
