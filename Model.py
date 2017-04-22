import sys
import OpenGL
from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *
import math
import random
import numpy as np


class Model:
    def __init__(self,filePath):
        #read the file and put information into correct places
        self.verticies = []
        self.triangles = []
        self.colors = []
        self.scale = [1,1,1]
        self.rotate = [0,0,0]
        self.patches = []
        self.resolution = None
        #format is [x0,y0,z0,x1,y1,y1,x2,y2,z2][....]
        self.bezierTriangles = []
        f = open(filePath, 'r')
        patch = []
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
                if splitLine[0] == "n":
                    self.resolution = int(splitLine[1])
                if splitLine[0] == "b":
                    patch.append([float(splitLine[1]),float(splitLine[2]),float(splitLine[3])])
                    if (len(patch)==16):
                        gbx = np.matrix([[patch[0][0],patch[1][0],patch[2][0],patch[3][0]],
                                         [patch[4][0],patch[5][0],patch[6][0],patch[7][0]],
                                         [patch[8][0],patch[9][0],patch[10][0],patch[11][0]],
                                         [patch[12][0],patch[13][0],patch[14][0],patch[15][0]]])

                        gby = np.matrix([[patch[0][1],patch[1][1],patch[2][1],patch[3][1]],
                                         [patch[4][1],patch[5][1],patch[6][1],patch[7][1]],
                                         [patch[8][1],patch[9][1],patch[11][1],patch[11][1]],
                                         [patch[12][1],patch[13][1],patch[14][1],patch[15][1]]])

                        gbz = np.matrix([[patch[0][2],patch[1][2],patch[2][2],patch[3][2]],
                                         [patch[4][2],patch[5][2],patch[6][2],patch[7][2]],
                                         [patch[8][2],patch[9][2],patch[12][2],patch[11][2]],
                                         [patch[12][2],patch[13][2],patch[14][2],patch[15][2]]])
                        patch = [gbx,gby,gbz]
                        self.patches.append(patch)
                        patch = []


        except IOError as e:
            print ("could not read Model error")
        finally:
            for patch in self.patches:
                print("new patch")
                for item in patch:
                    print(item)
            f.close()
            self.mapBezier()


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

        if(drawModel.triangles!=[]):
            #There is a normal model here. Draw it.
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
            #TODO update this to draw actual bezier stuff
            glEnd()
        glBegin(GL_TRIANGLES)
        color = 0
        colorScale = 1.0/len(self.bezierTriangles)
        for triangle in self.bezierTriangles:
            color = (color+colorScale)
            glColor3f(color,color,color)
            glVertex3f(triangle[0],triangle[1],triangle[2])
            glVertex3f(triangle[3],triangle[4],triangle[5])
            glVertex3f(triangle[6],triangle[7],triangle[8])
        #Here draw the cury stuff


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
    

    def mapBezier(self):
        self.bezierTriangles = []
        bezierBlock = []
        for patch in self.patches:
            bezierBlock.append(self.mapBezierPatch(patch))
        for patch in bezierBlock:
            for yIndex in range(len(patch[0])-1):
                for xIndex in range(len(patch[0])-1):
                    #make two triangles based off of this point.
                    #format is [x0,y0,z0,x1,y1,y1,x2,y2,z2][....]
                    x0 = patch[xIndex][yIndex][0]
                    y0 = patch[xIndex][yIndex][1]
                    z0 = patch[xIndex][yIndex][2]
                    x1 = patch[xIndex+1][yIndex][0]
                    y1 = patch[xIndex+1][yIndex][1]
                    z1 = patch[xIndex+1][yIndex][2]
                    x2 = patch[xIndex][yIndex+1][0]
                    y2 = patch[xIndex][yIndex+1][1]
                    z2 = patch[xIndex][yIndex+1][2]
                    x3 = patch[xIndex+1][yIndex+1][0]
                    y3 = patch[xIndex+1][yIndex+1][1]
                    z3 = patch[xIndex+1][yIndex+1][2]

                    triangle1 = [x0,y0,z0,x1,y1,z1,x3,y3,z3]
                    triangle2 = [x0,y0,z0,x2,y2,z2,x3,y3,z3]

                    self.bezierTriangles.append(triangle1)
                    self.bezierTriangles.append(triangle2)

            


    def mapBezierPatch(self,patch):
        #[[xyz of x0,y0],[xyz of x1,y0]...
        bezierCoordinates = []
        increment = 1.0/self.resolution
        for ySquareIndex in range(self.resolution+1):
            bezierLine = []
            for xSquareIndex in range(self.resolution+1):
                #create weights
                #find U (0-1)
                xWeight = xSquareIndex*increment
                yWeight = ySquareIndex*increment
                bi1 = (1-xWeight)**3
                bi2 = 3*xWeight*(1-xWeight)**2
                bi3 = 3*xWeight**2*(1-xWeight)
                bi4 = xWeight**3
                bi = [bi1,bi2,bi3,bi4]
                bj1 = (1-yWeight)**3
                bj2 = 3*yWeight*(1-yWeight)**2
                bj3 = 3*yWeight**2*(1-yWeight)
                bj4 = yWeight**3
                bj = [bj1,bj2,bj3,bj4]
                #calculate the sum
                point = [0,0,0]
                for x in range(4):
                    for y in range(4):
                        #patch[0]= x bezier
                        point[0] += patch[0][x,y] * bi[x] * bj[y]
                        point[1] += patch[1][x,y] * bi[x] * bj[y]
                        point[2] += patch[2][x,y] * bi[x] * bj[y]
                bezierLine.append(point)
            bezierCoordinates.append(bezierLine)
        return bezierCoordinates

            





