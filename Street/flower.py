from OpenGL.GL import *

flower = [
    "---12--",
    "-13213-",
    "134312-",
    "11112--",
    "-356---",
    "---7---",
    "---7---",
    "---7---",
    "56-8-66",
    "-5-55--",
    "--565--",]

flower_colors = {
    "1": (0.929, 0.188, 0.173),
    "2": (0.608, 0.133, 0.102),
    "3": (0.749, 0.145, 0.161),
    "4": (0.455, 0.137, 0.012),
    "5": (0.125, 0.275, 0.149),
    "6": (0.149, 0.353, 0.145),
    "7": (0.29, 0.561, 0.157),
    "8": (0.169, 0.439, 0.165)}



def begin_solid_draw():
    glPushAttrib(
        GL_CURRENT_BIT | GL_ENABLE_BIT | GL_LIGHTING_BIT | GL_TEXTURE_BIT | GL_LINE_BIT )


def end_solid_draw():
    glPopAttrib()


def draw_polygon(polygon, color=(1, 1, 1)):
    glLineWidth(1.0)
    glColor3f(*color)
    glBegin(GL_POLYGON)
    for point in polygon:
        glVertex3f(*point)
    glEnd()


def draw_pixel(x, y, size=0.05, color=(1, 0, 0)):
    polygon = [
        (x, y, 0),
        (x + size, y, 0),
        (x + size, y + size, 0),
        (x, y + size, 0),
    ]
    draw_polygon(polygon, color)


def draw_flower(origin_x=0, origin_y=0, pixel_size=0.05):
    begin_solid_draw()

    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glColor3f(1,1,1)

    for y, row in enumerate(flower):
        for x, cell in enumerate(row):
            if cell != "-":
                draw_pixel(
                    origin_x + x * pixel_size,
                    origin_y - y * pixel_size,
                    pixel_size,
                    flower_colors[cell]
                )

    end_solid_draw()


class Flower:
    @staticmethod
    def draw():
        glPushMatrix()
        draw_flower()
        glPopMatrix()
