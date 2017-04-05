
from Controller import * 
from View import *



myController = MyController()
myController.loadCameraFromMultiFile('cameras_05.txt')
myController.loadModel('./inputFiles/teapot.txt')
myView = MyView(myController)






glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
glutInitWindowSize(640, 640)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Hayes_Assignment_05")
glClearColor(1,0,0,0)
glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS);

lambdaDisp = lambda : myView.display()


glutDisplayFunc(lambdaDisp)






glutMainLoop()





