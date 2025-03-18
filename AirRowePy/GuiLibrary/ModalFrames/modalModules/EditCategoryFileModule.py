import tkinter.ttk
from math import floor

from AirRowePy.GuiLibrary.FileManager import FileManager
from AirRowePy.GuiLibrary.Frames.FrameWrapper import GridFrame, ScrollPackFrame

COMPONENT = 'C'
VAR = 'V'
OUTER_FRAME = 'O'
SCROLL = 'S'
INNER_FRAME='I'
FRAME='F'
LIST='L'
SHIFT_LEFT_BUTTON='l'
SHIFT_RIGHT_BUTTON='r'
COMMIT_BUTTON='c'

FILE_MANAGER="fileManager"
FILE_NAME="fileName"
FILE_EXT="extention"

bgColor1 = "#FFFFEE"
bgColor2 = "#FFFFAD"

class EditCategoryFileModule(GridFrame):
    def __init__(self, parent,resolve, unmappedVals, otherOptions={FILE_MANAGER:FileManager(FileManager.CATEGORY_FILES_PATH), FILE_NAME:"default", FILE_EXT:"txt"},
                 grid={"r": 0, "c": 0, "px": 0, "py": 0}) -> None:
        super().__init__(parent, grid=grid)
        self.fm = otherOptions["fileManager"]
        self.fileName = otherOptions["fileName"]
        self.ext = otherOptions["extention"]
        self.categoryMap = self.fm.loadCategoryFile(self.fileName, ext=self.ext)
        self.headerOrder = list(self.categoryMap.keys())
        self.lastHeaderIdx = len(self.headerOrder)-1
        self.unmappedVals = unmappedVals
        self.resolve = resolve

        self.headerComps = []
        self.listComps = []
        self.newListComps = []
        
        self.acceptButton=None

        self.render()

    def makeHeaderComp(self, header, rowIdx, colIdx):
        label = tkinter.Label(self.frame, text=header)
        label.grid(row=rowIdx, column=colIdx)
        return {
            COMPONENT:label
        }
    def makeListElementComp(self, parentFrame, val, rowIdx):
        label = tkinter.Label(parentFrame, text=val)
        label.grid(row=rowIdx)
        return {
            COMPONENT:label
        }
    
    def shiftElement(self, rowIdx, colIdx, left):
        srcCompsList = self.newListComps[colIdx][LIST]
        newColIdx = colIdx-1 if left else colIdx+1
        targetFrame = self.newListComps[newColIdx][FRAME]
        targetCompsList = self.newListComps[newColIdx][LIST]
        # if len(targetCompsList) == 0:
        #     self.newListComps[newColIdx][FRAME].grid(row=2,column=colIdx)
        #     print("Col Idx "+str(newColIdx)+"is now visible")

        #create new component from old one
        comps = srcCompsList.pop(rowIdx)
        # print("shifting colIdx="+str(colIdx)+" rowIdx="+str(rowIdx)+"val="+comps[VAR].get()+" to colIdx="+str(newColIdx)+" rowIdx="+str(len(targetCompsList))+".")
        targetCompsList.append(self.makeNewListElementComp(targetFrame,comps[VAR].get(),len(targetCompsList),newColIdx))
        #destroy old component
        comps[FRAME].destroy()
        #adjust grid spacing on old list
        for idx in range(rowIdx, len(srcCompsList)):
            srcCompsList[idx][FRAME].grid(row=idx)
        # if len(srcCompsList) == 0:
        #     self.newListComps[colIdx][FRAME].grid_forget()
        #     print("Col Idx "+str(colIdx)+"is now invisible")
        
    def commitElement(self, rowIdx, colIdx):
        srcCompsList = self.newListComps[colIdx][LIST]
        target=self.listComps[colIdx]
        #create new component from old one
        comps = srcCompsList.pop(rowIdx)
        val = comps[VAR].get()
        target[LIST].append(self.makeListElementComp(target[SCROLL][INNER_FRAME], val, len(target[LIST])))
        #destroy old component
        comps[FRAME].destroy()
        #adjust grid spacing on old list
        for idx in range(rowIdx, len(srcCompsList)):
            srcCompsList[idx][FRAME].grid(row=idx)
        # if len(srcCompsList) == 0:
        #     self.newListComps[colIdx][FRAME].grid_forget()
        #     print("Col Idx "+str(colIdx)+"is now invisible")
        self.categoryMap[self.headerOrder[colIdx]].append(val)
        
        
    def makeNewListElementComp(self, parentFrame, val, rowIdx, colIdx):
        frame = tkinter.Frame(parentFrame)
        shiftLeftButton = tkinter.Button(frame, text="<", command=lambda *args, rI=rowIdx, cI=colIdx: self.shiftElement(rI,cI,True)) if colIdx > 0 else tkinter.Button(frame, text="<", state='disabled', command=lambda *args: print("Can't move left"))
        shiftRightButton = tkinter.Button(frame, text=">", command=lambda *args, rI=rowIdx, cI=colIdx: self.shiftElement(rI,cI,False)) if colIdx < self.lastHeaderIdx else tkinter.Button(frame, text=">", state='disabled', command=lambda *args: print("Can't move right"))
        commitButton = tkinter.Button(frame, text="add", command=lambda *args, rI=rowIdx, cI=colIdx: self.commitElement(rI, cI))
        strVar=tkinter.StringVar(value=val)
        label=tkinter.Label(frame, textvariable=strVar)
        label.grid(row=0, column=1)
        commitButton.grid(row=1, column=1)
        shiftLeftButton.grid(row=0,column=0,rowspan=2,sticky="nsew")
        shiftRightButton.grid(row=0,column=2,rowspan=2,sticky="nsew")
        frame.grid(row=rowIdx, column=colIdx, pady=2)
        return {
            FRAME:frame,
            SHIFT_LEFT_BUTTON:shiftLeftButton,
            SHIFT_RIGHT_BUTTON:shiftRightButton,
            COMMIT_BUTTON:commitButton,
            VAR:strVar,
            COMPONENT:label
        }

    def makeValListScroll(self, valArray, rowIdx, colIdx):
        scrollOuterFrame = tkinter.Frame(self.frame)
        scrollOuterFrame.grid(row=rowIdx,column=colIdx)
        scrollComp = ScrollPackFrame(scrollOuterFrame, height=500, width=100)
        scrollInnerFrame = scrollComp.getInnerFrame()
        compList = []
        listIdx=0
        for val in valArray:
            compList.append(self.makeListElementComp(scrollInnerFrame, val, listIdx))
            listIdx+=1
        comps = {
            SCROLL:{
                OUTER_FRAME:scrollOuterFrame,
                COMPONENT:scrollComp,
                INNER_FRAME:scrollInnerFrame
            },
            LIST:compList
        }
        return comps

    def makeNewValListComp(self, newVals, rowIdx, colIdx):
        labelFrame = tkinter.LabelFrame(self.frame, text="",background=bgColor2)
        compList = []
        rIdx=0
        for val in newVals:
            compList.append(self.makeNewListElementComp(labelFrame, val, rIdx, colIdx))
            rIdx+=1
        # if rIdx > 0:
        labelFrame.grid(row=rowIdx,column=colIdx,sticky="ns")
        return {
            FRAME:labelFrame,
            LIST:compList
        }


    def render(self):
        numNewVals = len(self.unmappedVals) # =9
        numHeaders = len(self.headerOrder) # =8
        numNewValuesPerHeader = floor(numNewVals/numHeaders) # =1
        numlistsWithExtraNewValue = numNewVals%numHeaders # = 9%8 == 1
        colIdx = 0
        newValsIdx = 0
        newValsNextIdx = numNewValuesPerHeader+(1 if numlistsWithExtraNewValue > colIdx else 0)
        for header in self.headerOrder:
            rowIdx = 0
            self.headerComps.append(self.makeHeaderComp(header, rowIdx, colIdx))
            rowIdx+=1
            self.listComps.append(self.makeValListScroll(self.categoryMap[header], rowIdx, colIdx))
            rowIdx+=1
            self.newListComps.append(self.makeNewValListComp(self.unmappedVals[newValsIdx:newValsNextIdx], rowIdx, colIdx))
            rowIdx+=1
            self.acceptButton = tkinter.Button(self.frame, text="ACCEPT", command=self.resolve)
            self.acceptButton.grid(row=rowIdx, column=0,columnspan=self.lastHeaderIdx+1,sticky="nsew")
            newValsIdx = newValsNextIdx
            colIdx+=1
            newValsNextIdx += numNewValuesPerHeader+(1 if numlistsWithExtraNewValue > colIdx else 0)

    def destroy(self):
        for comps in self.listComps:
            comps[SCROLL][COMPONENT].destroy()
        super().destroy()
        
    def getValues(self):
        self.fm.saveCategoryFile(self.fileName, self.categoryMap, ext=self.ext)
        return self.categoryMap