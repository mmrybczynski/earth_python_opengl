
# I need install to next:
# pip install :
# pillow
# image
# pyopengl and acelerate pyopengl from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl
# the correct version to our python (I have python 3.7) 
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL.Image import *

import sys,gc


ESCAPE = '\033'

# Number of the glut window.
window = 0
rot = 0.0
rot3 = 0.0
rot6 = 0.0
LightAmb=(0.7,0.7,0.7)  
LightDif=(1.0,1.0,0.0)  
LightPos=(4.0,4.0,6.0,1.0)
#q=GLUquadricObj()
xrot=yrot=0.0

xrotspeed=yrotspeed=0.0 
zoom=-3.0
height=0.5 
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


# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):                # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glClearStencil(0)
    glDepthFunc(GL_LEQUAL)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading



    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_TEXTURE_2D)


    glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDif)
    glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
    glEnable(GL_LIGHT0)           
    glEnable(GL_LIGHTING)



    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix

                                                    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)



# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
  
def DrawEarth():
    global Q1
    glColor3f(1.0, 1.0, 1.0);
    glBindTexture( GL_TEXTURE_2D, LoadTextures('earthmap.bmp') )
    
    Q1=gluNewQuadric()
    gluQuadricNormals(Q1, GL_SMOOTH)
    gluQuadricTexture(Q1, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
    glPushMatrix()
    glTranslatef(0.0,0.0,4.0)			# Center The Cylinder
    gluSphere(Q1,0.40,32,16) 
    gluDeleteQuadric( Q1 )
    glPopMatrix()  

def DrawMoon():
    global Q2
    glColor3f(1.0, 1.0, 1.0);
    glBindTexture( GL_TEXTURE_2D, LoadTextures('earthmap.bmp') )
    
    Q2=gluNewQuadric()
    gluQuadricNormals(Q2, GL_SMOOTH)
    gluQuadricTexture(Q2, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
    glPushMatrix()
    glTranslatef(0.0,0.0,4.0)			# Center The Cylinder
    gluSphere(Q2,0.20,32,16) 
    gluDeleteQuadric( Q2 )
    glPopMatrix() 

def DrawGLScene():
    global rot, texture, rot3, rot6


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear The Screen And The Depth Buffer
    glLoadIdentity()  # Reset The View
    
    glTranslatef(0.0, -2.7, -20.0)  # Move Into The Screen

    glRotatef(-45, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot3, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    DrawEarth()

    glRotatef(-45, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    #glRotatef(0, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    DrawMoon()
    
    # Start Drawing The Cube
    rot = (rot + 0.16) % 360  # rotation
    rot3 = (rot3 + 0.12) % 360
    rot6 = -360
    
    
    
    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()


def main():
    global window
    glutInit(sys.argv)

    # Select type of Display mode:
    #  Double buffer
    #  RGBA color
    # Alpha components supported
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(612, 540)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)

    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("Ziemia")

    # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Initialize our window.
    InitGL(612, 540)

    # Start Event Processing Engine
    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
if __name__ == "__main__":
    main()















