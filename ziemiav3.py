import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

esfera_1 = {'center': (0, 0, 0), 'radius': 1, 'color': (1, 0, 0), 'angle': 0, 'axis': (0, 1, 0)}
esfera_2 = {'center': (3, 0, 0), 'radius': 0.5, 'color': (0, 1, 0), 'angle': 0, 'axis': (0, -1, 0)}

def calculate_points(esfera):
    points = []
    for i in range(0, 100):
        lat = ((i / 100) * math.pi) - (math.pi / 2)
        for j in range(0, 100):
            lon = (j / 100) * (2 * math.pi)

            x = esfera['center'][0] + (esfera['radius'] * math.cos(lat) * math.cos(lon))
            y = esfera['center'][1] + (esfera['radius'] * math.cos(lat) * math.sin(lon))
            z = esfera['center'][2] + (esfera['radius'] * math.sin(lat))
            points.append((x, y, z))
    return points

def draw_esfera(esfera):
    glBegin(GL_POINTS)
    for point in esfera['points']:
        glColor3fv(esfera['color'])
        glVertex3fv(point)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        esfera_1['points'] = calculate_points(esfera_1)
        esfera_2['points'] = calculate_points(esfera_2)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        glRotatef(esfera_1['angle'], esfera_1['axis'][0], esfera_1['axis'][1], esfera_1['axis'][2])
        draw_esfera(esfera_1)
        glPopMatrix()

        glPushMatrix()
        glRotatef(esfera_2['angle'], esfera_2['axis'][0], esfera_2['axis'][1], esfera_2['axis'][2])
        draw_esfera(esfera_2)
        glPopMatrix()

        esfera_1['angle'] = (esfera_1['angle'] + 1) % 360
        esfera_2['angle'] = (esfera_2['angle'] - 1) % 360

        esfera_2['center'] = (
            esfera_2['center'][0] * math.cos(math.radians(1)) - esfera_2['center'][1] * math.sin(math.radians(1)),
            esfera_2['center'][0] * math.sin(math.radians(1)) + esfera_2['center'][1] * math.cos(math.radians(1)),
            esfera_2['center'][2]
        )

        pygame.display.flip()
        pygame.time.wait(10)

main()
