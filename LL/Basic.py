# 1)
# Importa todas las funciones principales de OpenGL
from OpenGL.GL import *
# Utility. Contiene herramientas como "gluPerspective" y "gluLookAt"
from OpenGL.GLU import *
# GLUT. Manejo de eventos (main loop), ventanas, callbacks (funciones que llaman a GLUT)
from OpenGL.GLUT import *

#2)
# Tamaño de la ventana
w, h = 800, 600

# 5)
# Configuración inicial (o por defecto) de OpenGL
def init():
    # Define el color a usar cuando se llame a glClear
    glClearColor(0.1, 0.1, 0.1, 1.0)
    # Activa el buffer de profundidad (eje z), obligatorio si se usan objetos 3D
    glEnable(GL_DEPTH_TEST)

# 6)
# Define la función a realizar cuando se modifica el tamaño de la ventana
def reshape(width, height):
    # Para modificar las variables de tamaño en el código
    global w, h
    # Actualiza valores al nuevo tamaño
    w, h = width, max(height, 1)
    # Define la región donde OpenGL dibuja, en este caso es toda la ventana
    glViewport(0, 0, w, h)

# 7)
# Función para dibujar objetos en escena
def display():

    # PREPARAR ESCENARIO

    # Limpiar buffers, siempre se tiene que hacer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Selecciona la matriz a la que afectarán las siguientes configuraciones (PROJECTION: Perspectiva, MODELVIEW: camara y transformaciones)
    glMatrixMode(GL_PROJECTION)

    # Obligatorio
    glLoadIdentity()

    # Crea una proyección en perspectiva (como una cámara)
    # (FOV, aspect ratio, near_plane (Todo mas cerca que este valor no se dibuja), far_plane (lo contrario, todo lo mas lejano a este valor no se dibuja)
    # Se usa en aspect ratio w/h para que no se estire la escena
    gluPerspective(60.0, w/h, 0.1, 100.0)

    # Ahora se aplicarán las siguientes configuraciones a la cámara y modelo
    glMatrixMode(GL_MODELVIEW)

    # Obligatorio x2
    glLoadIdentity()

    # Define la posición de la cámara
    gluLookAt(
        0, 0, 3, # Posición de la camará en eje X Y Z
        0, 0, 0, # Desde esa posición, va a mirar a este punto X Y Z (0,0,0; para origen)
        0, 1, 0 # Desconocido... dejar asi o juguetear para entender
    )

    #DIBUJO EN LA ESCENA

    # Empieza a definir una lista de vertices (TRIANGLES: Cada 3 vertices dibuja 1 triángulo; QUADS: Cada 4 vertices dibuja 1 cuadrado; ...)
    glBegin(GL_TRIANGLES)

    glColor3f(1, 0, 0); glVertex3f(-1, -1, 0) # Color a aplicar al siguiente vértice creado; # Crear el vertice en las cc X Y Z
    glColor3f(0, 1, 0); glVertex3f( 1, -1, 0) # Verde
    glColor3f(0, 0, 1); glVertex3f(0, 1, 0) # Azul

    # Cierra la secuencia iniciada desde glBegin()
    glEnd()

    # Evita parpadeos (obligatorio)
    glutSwapBuffers()

# 8)
# Callback por GLUT cuando no hay eventos pendientes (libre)
def idle():
    # Mantiene la ventana animándose, sin este, display() solo se ejecuta cuando la ventana lo requiera
    glutPostRedisplay()


# 4)
# Crea ventana y conecta callbacks
def main():
    # Inicializa GLUT
    glutInit()

    #Doble buffer | Color en RGB | Buffer de profundidad (para DEPTH_TEST)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    # Tamaño inicial de la ventana
    glutInitWindowSize(w,h)

    #  Creación de la ventana
    glutCreateWindow(b"Learning OpenGL")

    # Se llama a OpenGL ya con la ventana y contexto creado
    init()

    # Llamar callbacks de GLUT
    # Callback cuando se necesite redimensionar
    glutReshapeFunc(reshape)
    # Callback cuando se necesite dibujar
    glutDisplayFunc(display)
    # Callback cuando GLUT no esté haciendo nada
    glutIdleFunc(idle)

    #Loop de GLUT. Procesa eventos, llama a los callbacks, mantiene la ventana ejecutándose
    glutMainLoop()

# 3)
# Evita el arranque del programa si es importado como módulo
if __name__ == "__main__":
    main()