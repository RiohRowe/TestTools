import tkinter
from ctypes.wintypes import VARIANT_BOOL

from AirRowePy.GuiLibrary.Frames.FrameWrapper import GridFrame

VAR='v'
COMPONENT='C'
TRACES = 'T'
ADD_BUTTON='A'
REMOVE_BUTTON='R'

bgColor1 = "#FFFFEE"
bgColor2 = "#FFFFAD"

class objectListComponent(GridFrame):
    def __init__(self, parent, content, index, headers=[], grid=None, addComponent=None, removeComponent=None, updateComponent=None):
        if not grid:
            grid={"r":index,"c":0}
        grid["px"]=10
        grid["py"]=1
        self.content = content
        self.index = index
        self.indexComponents = {}
        self.headerComponents = []
        self.buttonComponents = {}
        self.headers = list(headers)
        if addComponent:
            self.addComponentFunc = addComponent
        else:
            self.addComponentFunc = lambda:print("No implementation provided for addComponent.")
        if removeComponent:
            self.removeComponentFunc = removeComponent
        else:
            self.removeComponentFunc = lambda:print("No implementation provided for removeComponent.")
        if updateComponent:
            self.updateComponentFunc = updateComponent
        else:
            self.updateComponentFunc = lambda:print("No implementation provided for updateComponent.")
        def returnLabledComponent(parent, text=""):
            return tkinter.LabelFrame(parent, text=text)
        self.getComponent = returnLabledComponent

        super().__init__(parent, grid)
        self.render()

    def clearHeaderTraces(self, comps):
        for trace in comps[TRACES]:
            comps[VAR].trace_remove('write', trace)
        comps[TRACES] = []
    def setHeaderTrace(self, comps, header):
        comps[TRACES].append(comps[VAR].trace_add("write", lambda *args, key=header: print("index="+str(self.index)+"\tkey="+str(header))))
    def resetHeaderTrace(self, comps, header):
        self.clearHeaderTraces(comps)
        self.setHeaderTrace(comps, header)

    def setIndexes(self, gridIdx=None, gListIdx=None):
        if gridIdx != None:
            # print("Grid index now "+str(gridIdx))
            super().update({"r":gridIdx})
        if gListIdx!=None:
            # print("Global index was "+str(self.index)+" now "+str(gListIdx))
            self.index=gListIdx
            self.indexComponents[VAR].set(self.index)
            self.indexComponents[COMPONENT].configure(background=bgColor1 if self.index%2==0 else bgColor2)
    def createComps(self, idx, header):
        varVariable = tkinter.StringVar(value=self.content[header])
        inputComponent = tkinter.Entry(self.frame,
                                       textvariable=varVariable,
                                       width=20)
        inputComponent.grid(row=0,column=idx,padx=0,pady=0)
        comps = {
            VAR:varVariable,
            COMPONENT:inputComponent,
            TRACES:[]
        }
        self.setHeaderTrace(comps, header)
        return comps
    def destroyComps(self, comps):
        self.clearHeaderTraces(comps)
        comps[COMPONENT].destroy()
    def updateVals(self, newContent=None, headers=None):
        if newContent:
            self.content = newContent
            if not headers:
                for idx in range(0,len(self.headers)):
                    header = self.headers[idx]
                    comps = self.headerComponents[idx]
                    self.clearHeaderTraces(comps)
                    comps[VAR].set(self.content[header] if self.content.keys().__contains__(header) else "")
                    self.setHeaderTrace(comps, header)
                return
        if headers:
            deltaHeaderLength = len(headers)-len(self.headers)
            if deltaHeaderLength < 0: #remove components
                for idx in range(len(self.headers), len(headers), -1):
                    self.destroyComps(self.headerComponents.pop(idx))
            numExistingComps = len(self.headerComponents)
            for idx in range(0, numExistingComps): # change values in list
                header = self.headers[idx]
                comps = self.headerComponents[idx]
                self.clearHeaderTraces(comps)
                comps[VAR].set(self.content[header] if self.content.keys().__contains__(header) else "")
                self.setHeaderTrace(comps, header)
            for idx in range(numExistingComps, len(headers)): # create new comps
                header = self.headers[idx]
                self.headerComponents.append(self.createComps(idx, header))
            self.headers = headers
    def removeThis(self):
        print("remove"+str(self.index))
        self.removeComponentFunc(self.index)
    def addHere(self):
        print("add"+str(self.index))
        self.addComponentFunc(self.index)
    def getHeaderVal(self,headerIdx):
        return self.headerComponents[headerIdx][VAR].get()
    def render(self):
        idx=0
        self.indexComponents[VAR] = tkinter.IntVar(value=self.index)
        self.indexComponents[COMPONENT] = tkinter.Label(self.frame, textvariable=self.indexComponents[VAR], background=bgColor1 if self.index%2==0 else bgColor2)
        self.indexComponents[COMPONENT].grid(row=0,column=idx,padx=3,pady=0)
        # create new content
        idx+=1
        for header in self.headers:
            self.headerComponents.append(self.createComps(idx,header))
            idx+=1

        # create remove button
        removeButton = tkinter.Button(self.frame, text="-", command=self.removeThis)
        removeButton.grid(row=0,column=idx,padx=2,pady=1)
        self.buttonComponents[REMOVE_BUTTON] = removeButton
        idx+=1
        # create add button
        addHereButton = tkinter.Button(self.frame, text="+^", command=self.addHere)
        addHereButton.grid(row=0,column=idx,padx=2,pady=1)
        self.buttonComponents[ADD_BUTTON] = addHereButton
