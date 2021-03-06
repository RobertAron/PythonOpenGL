import sys
import OpenGL

from Camera import *
from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *



class MyView:

    def __init__(self,controllerReference):
        self.controllerReference = controllerReference



    def display_message(self,x,y,message,font_size=12):
        #for some reason this function isn't working
        #TODO come make text appear.
        glPushMatrix()
        glLoadIdentity()
        glColor3f( 1,1,0 ) 
        glRasterPos2f(-2,1.5)
        for ch in message:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ctypes.c_int( ord(ch) )) 
        glPopMatrix()





    def display(self):
        #create model must be called from the display function?
        #Don't completely understand openGL logic
        self.controllerReference.createModel()
        w=glutGet(GLUT_WINDOW_WIDTH)
        h=glutGet(GLUT_WINDOW_HEIGHT)
        for camera in self.controllerReference.cameras:


            glEnable(GL_SCISSOR_TEST)
            glScissor(int(camera.viewPort[0]*w),
                      int(camera.viewPort[1]*h),
                      int((camera.viewPort[2]-camera.viewPort[0])*w),
                      int((camera.viewPort[3]-camera.viewPort[1])*h))


            glClearColor(0.4,0.4,0.6,0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            #glFrustum()
            #frust is for perspective
            if(camera.type==CameraType.PARALLEL):
                glOrtho(camera.vrc[0],camera.vrc[1],camera.vrc[2],camera.vrc[3],camera.vrc[4],camera.vrc[5])
            else:
                glFrustum(camera.vrc[0],camera.vrc[1],camera.vrc[2],camera.vrc[3],camera.vrc[4],camera.vrc[5])
            gluLookAt(camera.eye[0],camera.eye[1],camera.eye[2],camera.lookAt[0],camera.lookAt[1],camera.lookAt[2],camera.vup[0],camera.vup[1],camera.vup[2])

            
            
            
            glMatrixMode(GL_MODELVIEW)




            #render model
            glViewport(int(camera.viewPort[0]*w),
                      int(camera.viewPort[1]*h),
                      int((camera.viewPort[2]-camera.viewPort[0])*w),
                      int((camera.viewPort[3]-camera.viewPort[1])*h))
            glCallList(2)
            glCallList(1)


            #this load in axis lines
            glLoadIdentity()


        glutSwapBuffers()
        glFlush()