
from Controller import * 
from View import *



myController = MyController()
myController.loadCameraFromMultiFile('cameras_05.txt')
myView = MyView(myController)






glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB)
glutCreateWindow(b"PyOpenGL Demo")
glutDisplayFunc(myView.display())


glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-1,1,-1,1,1,30)
gluLookAt(0,0,10,0,0,0,0,1,0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glutMainLoop()





