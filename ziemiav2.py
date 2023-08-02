import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL.Image import *

textures = {}

def LoadTextures(fname):
    if textures.get( fname ) is not None:
        return textures.get( fname )
    texture = textures[fname] = glGenTextures(1)
    image = open(fname)

    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBX", 0, -1)
    # Create Texture    
    glBindTexture(GL_TEXTURE_2D, texture)   # 2d texture (x and y size)
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    return texture

def DrawEarth():
    global Q1
    glColor3f(1.0, 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, LoadTextures('earthmap.bmp'))

    Q1 = gluNewQuadric()
    gluQuadricNormals(Q1, GL_SMOOTH)
    gluQuadricTexture(Q1, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glTranslatef(0.0, 0.0, 4.0)  # Przesunięcie na pozycję sfery
    glRotatef(angle_1, 0, 1, 0)  # Obrót sfery wokół własnej osi
    gluSphere(Q1, 0.40, 32, 16)
    glPopMatrix()

    glPushMatrix()
    glRotatef(angle_2, 0, 1, 0)  # Obrót sfery wokół pierwszej sfery
    glTranslatef(2.0, 0.0, 0.0)  # Przesunięcie na pozycję drugiej sfery
    glRotatef(angle_3, 0, 1, 0)  # Obrót drugiej sfery wokół własnej osi
    gluSphere(Q1, 0.20, 32, 16)
    glPopMatrix()
    gluDeleteQuadric(Q1)

# Inicjalizacja Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

glTranslatef(0.0, 0.0, -5)

angle_1 = 0.0  # Kąt obrotu pierwszej sfery wokół własnej osi
angle_2 = 0.0  # Kąt obrotu drugiej sfery wokół pierwszej sfery
angle_3 = 0.0  # Kąt obrotu drugiej sfery wokół własnej osi

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Sterowanie prędkością obrotu obiektów (zmiana wartości może dostosować prędkość)
    angle_1 += 1  # Prędkość obrotu pierwszej sfery
    angle_2 += 0.5  # Prędkość obrotu drugiej sfery wokół pierwszej sfery
    angle_3 += 2  # Prędkość obrotu drugiej sfery wokół własnej osi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    DrawEarth()
    pygame.display.flip()
    pygame.time.wait(10)
