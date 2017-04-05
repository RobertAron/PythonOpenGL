from Model import *
from Camera import *



class MyController:
    def __init__(self):
        self.model = None
        self.cameras = None
        self.modelPath = './inputFiles/teapot.txt'
        self.cameraPath = 'cameras_05.txt'



    def loadModel(self):
        self.model= Model(self.modelPath)
        return self.model
    
    def loadCameraFromMultiFile(self):
        self.cameras = Camera.loadMultiCameraFile(self.cameraPath)

        
    def rotationCall(self,rotationType,canvas,rotationSteps,rotationTheta):
        #Don't do anything on last call
        if rotationSteps==0:return

        thetaPerStep = rotationTheta/int(rotationSteps)
        #rotation type is 1,2,3:x,y,z
        if rotationType ==1:
            self.model.rotate_X(thetaPerStep)
        if rotationType ==2:
            self.model.rotate_Y(thetaPerStep)
        if rotationType ==3:
            self.model.rotate_Z(thetaPerStep)
        canvas.draw_Model(self.model,self.cameras)
        self.rootWidget.after(200,lambda: self.rotationCall(rotationType,canvas,rotationSteps-1,rotationTheta-thetaPerStep))

    def scaleCall(self,steps,a_Scale,s_Scale,all_Scale,scale_Type,canvasReference):
        if scale_Type == 1 :
            scale_amount = [all_Scale,all_Scale,all_Scale]
            around_point = [0,0,0]
        else:
            scale_amount = s_Scale
            around_point = a_Scale
        scale_amount_step = [math.pow(scale_amount[0],1/steps),math.pow(scale_amount[1],1/steps),math.pow(scale_amount[2],1/steps)]
        self.scaleCallAction(steps,scale_amount_step,around_point,canvasReference)

    def scaleCallAction(self,steps,scale_amount_step,around_point,canvasReference):
        #Don't run on the last call
        if steps == 0 : return

        #move the model to the center point
        self.model.translate(-around_point[0],-around_point[1],-around_point[2])
        #scale the Model
        self.model.nonuniform_scale(scale_amount_step[0],scale_amount_step[1],scale_amount_step[2])
        #move the model back to the center point
        self.model.translate(around_point[0],around_point[1],around_point[2])

        canvasReference.draw_Model(self.model,self.cameras)

        #increment the mult amount and decrement how many steps left


        steps = steps - 1
        self.rootWidget.after(200,lambda: self.scaleCallAction(steps,scale_amount_step,around_point,canvasReference))


    def tranlslateCall(self,steps,x,y,z,canvasReference):
        x = x/steps
        y = y/steps
        z = z/steps
        self.translationCallAction(steps,x,y,z,canvasReference)

    def translationCallAction(self,remainingsteps,x,y,z,canvasReference):
        if remainingsteps == 0: return
        self.model.translate(x,y,z)
        remainingsteps = remainingsteps - 1
        canvasReference.draw_Model(self.model,self.cameras)
        self.rootWidget.after(200,lambda: self.translationCallAction(remainingsteps,x,y,z,canvasReference))


    def flyCall(self,x1,y1,z1,x2,y2,z2,steps,canvasReference):
        for camera in self.cameras:
            camera.vrp = [x1,y1,z1]
        canvasReference.draw_Model(self.model,self.cameras)
        self.rootWidget.update()
        xchange = (x1-x2)/steps
        ychange = (y1-y2)/steps
        zchange = (z1-z2)/steps
        self.flyCallAction(xchange,ychange,zchange,steps,canvasReference)

    def flyCallAction(self,xChange,yChange,zChange,remainingSteps,canvasReference):
        if remainingSteps == 0:return
        for camera in self.cameras:
            x=camera.vrp[0]
            y=camera.vrp[1]
            z=camera.vrp[2]
            camera.vrp = [x-xChange,y-yChange,z-zChange]
        canvasReference.draw_Model(self.model,self.cameras)
        remainingSteps = remainingSteps-1
        self.rootWidget.after(200,lambda: self.flyCallAction(xChange,yChange,zChange,remainingSteps,canvasReference))

    def createModel(self):
        if self.model != None:
            self.model.create_model()

    def keyHandler(self,Key,MouseX,MouseY):
        print('keyHandler')
        if Key == b'n':
            browsedFile = filedialog.askopenfilename(filetypes=[("allfiles", "*"), ("pythonfiles", "*.txt")])
            self.modelPath = browsedFile
        elif Key ==b'd':
            self.loadModel()