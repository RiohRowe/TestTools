import csv
import os.path
import tkinter

from unicodedata import numeric

from .EditableStringListFromCsvFileSubComps.ListExpandOptionsComponent import ListExpandOptionsComponent
from .FrameWrapper import GridFrame, ScrollGridFrame
from AirRowePy.GuiLibrary.Frames.EditableStringListFromCsvFileSubComps.ObjectListComponent import objectListComponent
from ..FileManager import FileManager
from ..ModalFrames.ModalWrapper import ModalWrapper
from ..ModalFrames.modalModules.baseAddToListModalModule import BaseAddElementsModalModule


#
class EditableStringListFromFileComponent(GridFrame):

    def __init__(self, parentFrame, listName, fileName='', fileRootPath='', fileDelimiter='', grid=None, rangeStart=None, rangeEnd=None, rangeSize=None):
        self.listLabel = None
        if not type(grid) == {}.__class__:
            grid = {"r":0,"c":0}
        grid["px"]=10
        grid["py"]=10
        super().__init__(parentFrame, grid=grid)

        self.fileRootPath = fileRootPath if fileRootPath else os.path.abspath('.')
        self.fileName = fileName if fileName else os.listdir(self.fileRootPath)
        self.fileDelimiter = fileDelimiter if fileDelimiter else '\t'

        self.listName = listName
        self.listContent = self.loadFile()
        self.listComponents = []
        listContentLen=len(self.listContent)
        if len(self.listContent) > 0:
            self.headers = self.listContent[0].keys()
        else:
            self.headers = []

        self.fm = FileManager(self.fileRootPath)

        self.setRange(rangeStart,rangeEnd,rangeSize,listContentLen)
        print("listContentLen - "+str(listContentLen))
        print("rangeStart - "+str(self.rangeStart))
        print("rangeEnd - "+str(self.rangeEnd))
        self.titleFrame = tkinter.Frame(self.frame)
        self.titleFrame.grid(row=0,column=0,padx=10,pady=3)
        self.headerFrame = tkinter.Frame(self.frame)
        # self.headerFrame.grid(row=1,column=0,padx=34,pady=0, sticky="ew")
        self.headerFrame.grid(row=1,column=0,padx=(30,10),pady=0)
        self.outerlistFrame = tkinter.Frame(self.frame)
        self.outerlistFrame.grid(row=2,column=0,padx=10,pady=0)
        self.scrollFrameWrapper = ScrollGridFrame(self.outerlistFrame, width=(134*len(self.headers))+40+200)
        self.scrollFrame = self.scrollFrameWrapper.getInnerFrame()
        self.listFrame = tkinter.Frame(self.scrollFrame)
        self.listFrame.grid(row=1,column=0,padx=10,pady=0)
        self.expanderTop = ListExpandOptionsComponent(self.scrollFrame, self.rangeStart, False, self.expand, self.getNumDispl)
        self.expanderBottom = ListExpandOptionsComponent(self.scrollFrame, len(self.listContent) - self.rangeEnd - 1, True, self.expand, self.getNumDispl, grid={'r':2, 'c':0, 'px':0, 'py':0})
        self.optionsFrame = tkinter.Frame(self.frame, highlightbackground="black", highlightthickness=2)
        self.optionsFrame.grid(row=3,column=0,padx=10,pady=3)
        self.fullRefresh()

    def getNumDispl(self):
        return self.rangeEnd-self.rangeStart+1
    def insertManyElements(self,idx, newElements):
        for element in newElements:
            for header in self.headers:
                if not element.__contains__(header):
                    element[header]=""
        # update actual list
        oldListLen = len(self.listContent)
        numberAdded = len(newElements)

        # relativeInsertIdx = idx-stickyStart
        oldRangeStart = self.rangeStart
        oldRangeEnd=self.rangeEnd
        oldLen = oldRangeEnd-oldRangeStart+1
        prevLeftEleLen = idx-oldRangeStart
        prevRightEleLen = oldLen-prevLeftEleLen
        #if the number of added elements is smaller or equal to the number of elements prior to the insert index...
        self.listContent = self.listContent[0:idx] + newElements + self.listContent[idx:]
        # if (oldListLen-1)-idx >= numberAdded:
        #     splitIdx = len(self.listContent) - numberAdded
        #     for rIdx in range(splitIdx, oldListLen):
        #         self.listContent.append(self.listContent[rIdx])
        #     for rIdx in range(idx, splitIdx):
        #         self.listContent[rIdx+numberAdded] = self.listContent[rIdx]
        #     for rIdx in range(0, numberAdded):
        #         self.listContent[idx+rIdx] = newElements[rIdx]
        # else:
        #     splitIdx = (oldListLen)-idx
        #     for rIdx in range(splitIdx, numberAdded):
        #         self.listContent.append(newElements[rIdx])
        #     for rIdx in range(idx,oldListLen):
        #         self.listContent.append(self.listContent[rIdx])
        #     for rIdx in range(0, splitIdx):
        #         self.listContent[idx+rIdx]=newElements[rIdx]
        #update displayed list
        roomNeeded = numberAdded # room needed to properly insert new elements
        newRangeStart = self.rangeStart
        print("newRangeStart = "+str(newRangeStart))
        newRangeEnd = self.rangeEnd
        # val = number of components to the right of the insert index that can be reused
        val = roomNeeded if prevRightEleLen > roomNeeded else prevRightEleLen-1 # pull from right
        print("val1="+str(val))
        print("roomNeeded="+str(roomNeeded)+"\tprevRightEleLen="+str(prevRightEleLen))
        roomNeeded -= val
        if roomNeeded > 0: # if can't pull entirely from the right
            # pull from left
            val = roomNeeded if prevLeftEleLen > roomNeeded else prevLeftEleLen - 1
            print("val2="+str(val))
            roomNeeded -= val
            newRangeStart += val
            newRangeEnd += val+roomNeeded #Take Excess from right

        remainingComps=self.rangeEnd-self.rangeStart+1
        #preserveLeftComps
        fromIdx = newRangeStart-self.rangeStart
        toIdx = 0
        print("newRangeStart="+str(newRangeStart)+"\tidx="+str(idx))
        for rIdx in range(newRangeStart, idx):
            print("from="+str(fromIdx)+"\tto="+str(toIdx))
            temp = self.listComponents[toIdx]
            self.listComponents[toIdx] = self.listComponents[fromIdx]
            self.listComponents[fromIdx] = temp
            self.listComponents[toIdx].setIndexes(gridIdx=toIdx)
            fromIdx+=1
            toIdx+=1
        remainingComps-=toIdx
        gridIdx=toIdx
        #alterInsertedComps
        for rIdx in range(idx, idx+remainingComps):
            print(rIdx)
            self.listComponents[gridIdx].setIndexes(gridIdx=gridIdx, gListIdx=rIdx)
            self.listComponents[gridIdx].updateVals(newContent=self.listContent[rIdx])
            gridIdx+=1
        #addAdditionalComps
        for rIdx in range(idx+remainingComps, newRangeEnd+1):
            self.listComponents.append(objectListComponent(self.listFrame, self.listContent[rIdx], rIdx, self.headers, grid={"r":gridIdx, "c":0, "px":0, "py":0}, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit))
            gridIdx+=1
        numCompsAbove = newRangeStart
        numCompsBelow = len(self.listContent)-newRangeEnd-1
        self.expanderTop.setNumHidden(numCompsAbove)
        self.expanderBottom.setNumHidden(numCompsBelow)
        if numCompsAbove == 0:
            self.expanderTop.hideExpand()
        else:
            self.expanderTop.showExpand()
        if numCompsBelow == 0:
            self.expanderBottom.hideExpand()
        else:
            self.expanderBottom.showExpand()
        self.expanderTop.showShrink()
        self.expanderBottom.showShrink()
        self.rangeStart = newRangeStart
        self.rangeEnd = newRangeEnd


    def expand(self, amount, expandDirDown):
        if expandDirDown:
            if amount>0: #Add Components to bottom and expand rangeEnd
                rangeGList = range(self.rangeEnd+1, self.rangeEnd+1+amount,1)
                rangeGrid = range(len(self.listComponents),len(self.listComponents)+amount)
                for gridIdx, gListIdx in zip(rangeGrid, rangeGList):
                    #create element
                    component = objectListComponent(self.listFrame, self.listContent[gListIdx], gListIdx, self.headers, grid={"r":gridIdx, "c":0, "px":0, "py":0}, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit)
                    #prepend new element
                    self.listComponents.append(component)

                #Adjust expand/contract ability
                if self.rangeStart == self.rangeEnd:
                    self.expanderTop.showShrink()
                    self.expanderBottom.showShrink()
                self.rangeEnd+=amount
                if self.rangeEnd+1 == len(self.listContent):
                    self.expanderBottom.hideExpand()
            else: #Remove Components from bottom and shrink rangeEnd
                rangeGrid = range(0,-amount)
                for gridIdx in rangeGrid:
                    #pop and destroy element
                    self.listComponents.pop().destroy()

                if self.rangeEnd+1 == len(self.listContent):
                    self.expanderBottom.showExpand()
                self.rangeEnd+=amount
                if self.rangeStart == self.rangeEnd:
                    self.expanderTop.hideShrink()
                    self.expanderBottom.hideShrink()
        else:
            if amount>0: #Prepend Components to beginning and adjust rangeStart
                newCompArr = []
                for gridIdx, gListIdx in enumerate(range(self.rangeStart-amount, self.rangeStart,1)):
                    #create element
                    component = objectListComponent(self.listFrame, self.listContent[gListIdx], gListIdx, self.headers, grid={"r":gridIdx, "c":0, "px":0, "py":0}, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit)
                    newCompArr.append(component)
                newGridIdx = amount
                for gridIdx in range(0, len(self.listComponents)):
                    component = self.listComponents[gridIdx]
                    component.setIndexes(gridIdx=newGridIdx)
                    newGridIdx+=1
                print(len(newCompArr))
                print(len(self.listComponents))
                self.listComponents = newCompArr+self.listComponents
                print("NEW GRID SIZE ="+str(len(self.listComponents)))

                if self.rangeStart == self.rangeEnd:
                    self.expanderTop.showShrink()
                    self.expanderBottom.showShrink()
                self.rangeStart-=amount
                if self.rangeStart == 0:
                    self.expanderTop.hideExpand()

            else: #Remove and destroy
                removedComps = self.listComponents[0:-amount]
                self.listComponents = self.listComponents[-amount:]
                #fix gid of preexisting elements
                for idx in range(0, len(removedComps)):
                    removedComps.pop().destroy()

                if self.rangeStart == 0:
                    self.expanderTop.showExpand()
                self.rangeStart-=amount
                if self.rangeStart == self.rangeEnd:
                    self.expanderTop.hideShrink()
                    self.expanderBottom.hideShrink()


    def destroy(self):
        super().destroy()
        self.titleFrame.destroy()
        self.headerFrame.destroy()
        self.expanderTop.destroy()
        self.expanderBottom.destroy()
        self.scrollFrame.destroy()
        self.outerlistFrame.destroy()
        self.optionsFrame.destroy()

    def edit(self, childIndex, key, newValue):
        if key in self.headers and len(self.listContent) > childIndex:
            #Update overall list
            self.listContent[childIndex][key]=newValue
            #Update component
            # self.listComponents[childIndex].updateValue(key, newValue)
    def adjustRange(self, start=0, end=0):
        self.rangeStart+=start
        self.rangeEnd+=end
        success = True
        if self.rangeStart < 0:
            self.rangeStart = 0
            success=False
        if self.rangeEnd >= len(self.listContent):
            self.rangeEnd = len(self.listContent-1)
            success=False
        return success

    #Only adjusts the range values and performs validations on the new values
    #Does not change the displayed components
    def setRange(self, startIdx=None, endIdx=None, size=None, contentSize=0):
        if not startIdx == None:
            #if startIndex is out of bounds, set to default
            if startIdx < 0 or startIdx >= contentSize:
                self.rangeStart = 0
            else:
                self.rangeStart = startIdx
            if not size == None:
                #if size is out of bounds
                if size < 1 or self.rangeStart + size > contentSize:
                    self.rangeEnd = contentSize-1
                else:
                    self.rangeEnd = self.rangeStart + (size-1)
            else:
                #if endIdx is out of bounds
                if endIdx < 0 or endIdx > contentSize-self.rangeStart:
                    self.rangeEnd = contentSize-1
                else:
                    self.rangeEnd = contentSize-1-endIdx
        else: #If endIdx is null, or out of bounds, set default value
            if endIdx == None or endIdx < 0 or endIdx >= contentSize:
                self.rangeEnd = contentSize-1
            else:
                self.rangeEnd = contentSize-1-endIdx
                #if size is out of bounds or None, set StartIndex to default value
            if size == None or size < 1 or self.rangeEnd - size < -1:
                self.rangeStart = 0
            else:
                self.rangeStart = self.rangeEnd - (size-1)

    #Remove row from global list
    #Remove row from displayed components
    #adjust indexes
    #try to replace with row from global list. Try right, then left.
    #Update expandComponents appropriately
    def remove(self, gListRemIndex):
    #remove from master list
        self.listContent.pop(gListRemIndex)
        gridListRemIdx = gListRemIndex-self.rangeStart
    #remove from component list
        removedComponent = self.listComponents.pop(gridListRemIdx)
        moreElementsToRight = self.rangeEnd < len(self.listContent)-1
    #Shift Indexes Left and try to insert from Right
        if self.rangeStart <=0 or moreElementsToRight:
            gridRange=range(gridListRemIdx, len(self.listComponents), 1)
            globalListRange=range(gListRemIndex, self.rangeEnd+1, 1)
    #Update remaining component index info
            for gridIdx, gListIdx in zip(gridRange, globalListRange):
                self.listComponents[gridIdx].setIndexes(gridIdx=gridIdx, gListIdx=gListIdx)
    # attempt to add component from right of global list
            if moreElementsToRight:
                component = objectListComponent(self.listFrame, self.listContent[self.rangeEnd], self.rangeEnd, self.headers, grid={"r": len(self.listComponents) - 1, "c":0, "px":0, "py":0}, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit)
                self.listComponents.append(component)
    #Update expand Element
                numhiddenRight = self.expanderBottom.numHidden-1
                self.expanderBottom.setNumHidden(numhiddenRight)
                if numhiddenRight == 0:
                    self.expanderBottom.hideExpand()
    #no more elements to fill range with. Decrease range size
            else:
                self.rangeEnd -= 1
                if self.rangeStart == self.rangeEnd:
                    self.expanderTop.hideShrink()
                    self.expanderBottom.hideShrink()
    #Shift Indexes and Try to insert from left of global list
        else: # fix grid layout of existing components and insert from left of global list
            self.rangeStart -= 1
            #insert new component with
            component = objectListComponent(self.listFrame, self.listContent[self.rangeStart], self.rangeStart, self.headers, grid={"r":0, "c":0, "px":0, "py":0}, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit)
            self.listComponents.insert(0, component)
            gridRange=range(1, len(self.listComponents), 1)
            globalListRange=range(self.rangeStart+1, self.rangeEnd+1, 1)
            self.rangeEnd -= 1
            #update remaining component index info
            for gridIdx, gListIdx in zip(gridRange, globalListRange):
                # print('global('+str(self.listComponents[gridIdx].index)+"->"+str(gListIdx)+")\tgrid("+str(self.listComponents[gridIdx].frame.grid_info()['row'])+"->"+str(gridIdx)+")")
                self.listComponents[gridIdx].setIndexes(gridIdx=gridIdx, gListIdx=gListIdx)
            self.expanderTop.setNumHidden(self.rangeStart)
            if self.rangeStart == 0:
                self.expanderTop.hideExpand()
        removedComponent.destroy()


    def append(self, newEntries=[]):
        oldLength = self.rangeEnd-self.rangeStart+1
        oldContentLen = len(self.listContent)
        #append to global list
        self.listContent = self.listContent + newEntries
        oldRangeEnd = self.rangeEnd
        self.rangeEnd = len(self.listContent)

        sizeIncrease = len(newEntries)

        newRangeStart = self.rangeEnd-sizeIncrease if sizeIncrease > oldLength else self.rangeEnd-oldLength
        overlap = oldRangeEnd-newRangeStart+1
        #adjust existing components
        newCompList = []
        if overlap > 0:
            #Adjust and position overlapping components
            newGridIdx = overlap-1
            for idx in range(oldLength-overlap, oldLength):
                comp = self.listComponents.pop()
                comp.setIndexes(gridIdx=newGridIdx)
                newCompList.append(comp)
                newGridIdx-=1
            #Append and Adjust contents of unused components
            newCompList += self.listComponents
            newGlobalIdx = oldContentLen
            for idx in range(overlap, len(newCompList)):
                newCompList[idx].setIndexes(gridIdx=idx, gListIdx=newGlobalIdx)
                newCompList[idx].updateVals(newContent=self.listContent[newGlobalIdx])
                newGlobalIdx+=1
            self.listComponents = newCompList
            #Create and add remaining components.
            for idx in range(oldLength,self.rangeEnd+1):
                self.listComponents.append(objectListComponent(
                    self.listFrame,
                    self.listContent[newGlobalIdx],
                    newGlobalIdx,
                    self.headers,
                    grid={"r":idx, "c":0, "px":0, "py":0},
                    addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit))
                newGlobalIdx+=1
        else:
            #adjust existing components
            newGlobalIdx = self.rangeStart
            for idx in range(0, self.listComponents):
                newCompList[idx].setIndexes(gridIdx=idx, gListIdx=newGlobalIdx)
                newCompList[idx].updateVals(newContent=self.listContent[newGlobalIdx])
                newGlobalIdx+=1
            self.listComponents = newCompList
            #Create and add remaining components.
            for idx in range(oldLength,self.rangeEnd+1):
                self.listComponents.append(objectListComponent(
                    self.listFrame,
                    self.listContent[newGlobalIdx],
                    newGlobalIdx,
                    self.headers,
                    grid={"r":idx, "c":0, "px":0, "py":0},
                    addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit))
                newGlobalIdx+=1

    def add(self, idx):
        defaultEntry = {}
        headerIdx = 0
        for header in self.headers:
            defaultEntry[header]={
                "type":"t",
                "editable":True,
                "defaultValue":self.listContent[idx][header]
            }
            headerIdx+=1
        addElementsModal = ModalWrapper(BaseAddElementsModalModule, "addToListModal", [defaultEntry],
                                        handleResolveValue= lambda *args, value: self.insertManyElements(idx, value) if idx < len(self.listContent) else self.append(value))


    def sortBy(self,key,asc=True):
        if key in self.headers:
            self.listContent = sorted(self.listContent, key=lambda listElement: listElement[key], reverse=asc)
            if self.rangeStart == 0 and self.rangeEnd == self.listContent.__len__()-1:
                self.listComponents = sorted(self.listComponents, key=lambda listElement: listElement.value()[key], reverse=asc)
                for index in range(0, len(self.listComponents),1):
                    self.listComponents[index].setIndexes(gridIdx=index, gListIdx=self.rangeStart+index)
            else:
                self.fullRefresh()
    def tupleFromDate(date, delimiter, dateFormatMap):
        dfa = date.split(delimiter)
        return (dfa[dateFormatMap["y"]],dfa[dateFormatMap["m"]],dfa[dateFormatMap["d"]])
    def sortByDate(self,key,asc=True,delimiter="/",format="m,d,y"):
        dateformat = format.split(",")
        dateFormatMap = {
            "y":dateformat.index("y"),
            "m":dateformat.index("m"),
            "d":dateformat.index("d")
        }
        if key in self.headers:
            self.listContent = sorted(self.listContent, key=lambda listElement, deli=delimiter, dfm=dateFormatMap: self.tupleFromDate(listElement[key], deli, dfm), reverse=asc)
            if self.rangeStart == 0 and self.rangeEnd == self.listContent.__len__()-1:
                self.listComponents = sorted(self.listComponents, key=lambda listElement, deli=delimiter, dfm=dateFormatMap: self.tupleFromDate(listElement.value()[key], deli, dfm), reverse=asc)
                for index in range(0, len(self.listComponents),1):
                    self.listComponents[index].setIndexes(gridIdx=index, gListIdx=self.rangeStart+index)
            else:
                self.fullRefresh()
    def move(self, childIndex, up):
        arrlen = len(self.listContent)
        if not childIndex < arrlen or childIndex < 0:
            return
        if (up and childIndex == 0) or (not up and childIndex == arrlen-1):
            return
        swapWithIndex = childIndex-1 if up else childIndex+1
        #swap elements in master list
        temp = self.listContent[childIndex]
        self.listContent[childIndex] = self.listContent[swapWithIndex]
        self.listContent[swapWithIndex] = temp
        #swap components in component list
        compTargetIdx = childIndex-self.rangeStart
        compSwapWithIdx = swapWithIndex-self.rangeStart
        temp = self.listComponents[compTargetIdx]
        self.listComponents[compTargetIdx] = self.listComponents[compSwapWithIdx]
        self.listComponents[compSwapWithIdx] = temp
        self.listComponents[compTargetIdx].setIndexes(gridIdx=compTargetIdx, gListIdx=childIndex)
        self.listComponents[compSwapWithIdx].setIndexes(gridIdx=compSwapWithIdx, gListIdx=swapWithIndex)

    def update(self, listName="", listContent=None, position=None, rangeStart=None, rangeEnd=None):
        if listContent and type(listContent) == [].__class__:
            self.listContent = listContent
            self.headers = []
            if len(listContent) > 0:
                self.headers = listContent[0].keys()
        if listName:
            self.listName = listName
        if position:
            super().update(position)
        if numeric(rangeStart):
            self.rangeStart = rangeStart
        if numeric(rangeEnd):
            self.rangeEnd = rangeEnd
    # fully deletes all child objects in list and recreates them based on new list values
    def fullRefresh(self):

        self.listComponents=[]
        if self.listLabel:
            self.listLabel.destroy()

        self.listLabel = tkinter.Label(self.titleFrame, text=self.listName)
        self.listLabel.grid(row=0,column=0,padx=10,pady=20)
        for idx, header in enumerate(self.headers):
            print(str(idx)+" - "+header)
            headerLabel = tkinter.Label(self.headerFrame, text=header, width=17, anchor="w", borderwidth=1, relief="groove")
            headerLabel.grid(row=0,column=idx,padx=(2,0),pady=0)
        idx = len(self.headers)
        loadButton = tkinter.Button(self.headerFrame, text="Load", command=self.reloadFromFile)
        loadButton.grid(row=0,column=idx,padx=(5,0),pady=0)
        idx+=1
        saveButton = tkinter.Button(self.headerFrame, text="Save", command=self.saveToFile)
        saveButton.grid(row=0,column=idx,padx=(5,0),pady=0)

        #create new children
        # for idx, content in enumerate(self.listContent):
        # print("contents")
        # print(self.listContent)
        # print(" ------- "+str(self.rangeStart)+"-"+str(self.rangeEnd)+" ------- ")
        for gridIdx, gListIdx in enumerate(range(self.rangeStart, self.rangeEnd+1, 1)):
            #create children components
            label = objectListComponent(self.listFrame, self.listContent[gListIdx], gListIdx, self.headers, grid={"r":gridIdx, "c":0, "px":0, "py":0}, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit)
            self.listComponents.append(label)
        # print("components")
        # print(self.listComponents)
    def reloadFromFile(self):
        self.listContent = self.fm.loadTableFile(self.fileName)
        self.fullRefresh()
        print("file loaded")
    def saveToFile(self):
        self.fm.saveTableFile(self.fileName)
        print("file saved")
    def loadFile(self):
        with open(os.path.join(self.fileRootPath, self.fileName), 'r') as datasource_file:
            return list(csv.DictReader(datasource_file, delimiter=self.fileDelimiter))

    def saveFile(self, listContents):
        with open(os.path.join(self.fileRootPath, self.fileName), 'w', newline='') as datasource_file:
            writer = csv.DictWriter(datasource_file, fieldnames=self.headers, delimiter=self.fileDelimiter)
            writer.writeheader()
            writer.writerows(listContents)

