import sys
import OpenGL

from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *

class MyView:

    def __init__(self,controllerReference):
        self.controllerReference = controllerReference





    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)

        #draw a triangle
        glBegin(GL_TRIANGLES)
        glColor3f(1,0,0)
        glVertex3f(-1,0,0)
        glVertex3f(1,0,0)
        glVertex3f(0,1,0)
        glEnd()



        glFlush()
        glutSwapBuffers()
        return self.display()