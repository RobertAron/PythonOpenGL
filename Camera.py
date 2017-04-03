from enum import Enum
import os

class CameraType(Enum):
    PARALLEL = 0
    PERSPECTIVE = 1



class Camera:
    def __init__(self,filePath):
        #i
        self.cameraName = ""
        #t (parallel or perspective)
        self.type = CameraType.PARALLEL
        #e
        self.eye = [0,0,0]
        #l
        self.lookAt = [0,0,1]
        #u
        self.vup = [0,1,0]
        #w <umin><umax><vmin><vnax><nmin><nmax>
        self.vrc = [-1,1,-1,1,-1,1]
        #s viewport <xmin><ymin><xmax><ymax
        self.viewPort = [.1,.1,.4,.4]
        f = open(filePath,'r')
        try:
            for line in f:
                splitLine = line.split()
                if splitLine == [] or splitLine == "":
                    break
                if splitLine[0] == "i":
                    self.cameraName = splitLine[1]
                if splitLine[0] == "t":
                    if splitLine[1]=="parallel":
                        self.type = CameraType.PARALLEL
                    else:
                        self.type = CameraType.PERSPECTIVE
                if splitLine[0] == "e":
                    self.eye = [float(splitLine[1]),float(splitLine[2]),float(splitLine[3])]
                if splitLine[0] == "l":
                    self.lookAt = [float(splitLine[1]),float(splitLine[2]),float(splitLine[3])]
                if splitLine[0] == "u":
                    self.vup == [float(splitLine[1]),float(splitLine[2]),float(splitLine[3])]
                if splitLine[0] == "w":
                    self.vrc = [float(splitLine[1]),float(splitLine[2]),float(splitLine[3]),float(splitLine[4]),float(splitLine[5]),float(splitLine[6])]
                if splitLine[0] == "s":
                    self.viewPort = [float(splitLine[1]),float(splitLine[2]),float(splitLine[3]),float(splitLine[4])]
        except IOError as e:
            print("could not read Camera Error")
        finally:
            f.close()


    @staticmethod
    def loadMultiCameraFile(filePath):
        cameraArray = []
        f = open(filePath,'r')
        tempFile = open('tempFile.txt','w')
        try:
            for line in f:
                tempFile.write(line)
                splitLine = line.split()
                if splitLine[0]=="s":
                    tempFile.close()
                    cameraArray.append(Camera("tempFile.txt"))
                    os.remove('tempFile.txt')
                    tempFile = open("tempFile.txt",'w')
            tempFile.close()
            os.remove('tempFile.txt')
            return cameraArray
        except IOError as e:
            print("could not read Camera Error")
        finally:
            f.close()
