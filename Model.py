import sys
import OpenGL
from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *
import math
import random


class Model:
    def __init__(self,filePath):
        #read the file and put information into correct places
        self.verticies = []
        self.triangles = []
        self.colors = []
        self.scale = [1,1,1]
        self.rotate = [0,0,0]
        f = open(filePath, 'r')
        try:
            for line in f:
                splitLine = line.split()
                if splitLine == [] or splitLine== "":
                    break
                if splitLine[0]== "v":
                    self.verticies.append([float(splitLine[1]),float(splitLine[2]),float(splitLine[3])])
                if splitLine[0]== "f":
                    triangle = []
                    color1 = []
                    color2 = []
                    color3 = []

                    #generate some colors for the pot
                    #currently random
                    color1 = random.uniform(0,1)
                    color2 = random.uniform(0,1)
                    color3 = random.uniform(0,1)
                    self.colors.append([color1,color2,color3])



                    #add the vectexes to the path
                    for index in range(1,len(splitLine)):
                        triangle.append(int(splitLine[index])-1)
                    self.triangles.append(triangle)

        except IOError as e:
            print ("could not read Model error")
        finally:
            f.close()


    def rotate_X(self,theta):
        self.rotate[0]+=theta
        #for i in range(len(self.verticies)):
        #    self.verticies[i] = [self.verticies[i][0],self.verticies[i][1]*math.cos(theta)-self.verticies[i][2]*math.sin(theta),self.verticies[i][1]*math.sin(theta)+self.verticies[i][2]*math.cos(theta)]

    def rotate_Y(self,theta):
        self.rotate[1]+=theta
        #for i in range(len(self.verticies)):
        #    self.verticies[i] = [self.verticies[i][0]*math.cos(theta)+self.verticies[i][2]*math.sin(theta),self.verticies[i][1],-self.verticies[i][0]*math.sin(theta)+self.verticies[i][2]*math.cos(theta)]


    def rotate_Z(self,theta):
        self.rotate[2] += theta
        #for i in range(len(self.verticies)):
        #    self.verticies[i] = [self.verticies[i][0]*math.cos(theta)-self.verticies[i][1]*math.sin(theta),self.verticies[i][0]*math.sin(theta)+self.verticies[i][1]*math.cos(theta),self.verticies[i][2]]


    def translate(self,x,y,z):
        for i in range(len(self.verticies)):
            self.verticies[i] = [self.verticies[i][0]+x,self.verticies[i][1]+y,self.verticies[i][2]+z]

    def nonuniform_scale(self,x_scale,y_scale,z_scale):
        self.scale = [self.scale[0]*x_scale,
                      self.scale[1]*y_scale,
                      self.scale[2]*z_scale]
        #for i in range(len(self.verticies)):
        #    self.verticies[i] = [self.verticies[i][0]*x_scale,self.verticies[i][1]*y_scale,self.verticies[i][2]*z_scale]


    def create_model(self):
        #drawModel = self.controllerReference.model
        drawModel = self
        #Draw the item
        glNewList(1,GL_COMPILE)
        #alternatively GL_POLYGON or GL_POINTS
        glRotatef(self.rotate[0],1,0,0)
        glRotatef(self.rotate[1],0,1,0)
        glRotatef(self.rotate[2],0,0,1)
        glScalef(self.scale[0],self.scale[1],self.scale[2])

        if(len(drawModel.triangles[0])==3):
            glBegin(GL_TRIANGLES)
            for index in range(len(drawModel.triangles)):
                triangle = drawModel.triangles[index]
                color = self.colors[index]
                glColor3f(color[0],color[1],color[2])
                glVertex3f(drawModel.verticies[triangle[0]][0],
                            drawModel.verticies[triangle[0]][1],
                            drawModel.verticies[triangle[0]][2])
                glVertex3f(drawModel.verticies[triangle[1]][0],
                            drawModel.verticies[triangle[1]][1],
                            drawModel.verticies[triangle[1]][2])
                glVertex3f(drawModel.verticies[triangle[2]][0],
                            drawModel.verticies[triangle[2]][1],
                            drawModel.verticies[triangle[2]][2])

        else:
            glBegin(GL_QUADS)
            for index in range(len(drawModel.triangles)):
                triangle = drawModel.triangles[index]
                color = self.colors[index]
                glColor3f(color[0],color[1],color[2])
                glVertex3f(drawModel.verticies[triangle[0]][0],
                            drawModel.verticies[triangle[0]][1],
                            drawModel.verticies[triangle[0]][2])
                glVertex3f(drawModel.verticies[triangle[1]][0],
                            drawModel.verticies[triangle[1]][1],
                            drawModel.verticies[triangle[1]][2])
                glVertex3f(drawModel.verticies[triangle[2]][0],
                            drawModel.verticies[triangle[2]][1],
                            drawModel.verticies[triangle[2]][2])
                glVertex3f(drawModel.verticies[triangle[3]][0],
                            drawModel.verticies[triangle[3]][1],
                            drawModel.verticies[triangle[3]][2])

        glEnd()
        glEndList()


    def create_3d_axes(self):
        glNewList(2,GL_COMPILE)
        glBegin(GL_LINES)
        glColor3f(1,0,0)
        glVertex3f(0,0,0)
        glVertex3f(2,0,0)
        glEnd() 
        
        glBegin(GL_LINES)
        glColor3f(0,1,0)
        glVertex3f(0,0,0)
        glVertex3f(0,2,0)
        glEnd() 
        
        glBegin(GL_LINES)
        glColor3f(0,0,1)
        glVertex3f(0,0,0)
        glVertex3f(0,0,2)
        glEnd() 
        glEndList()    