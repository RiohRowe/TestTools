import csv
import os.path
import tkinter

from unicodedata import numeric

from .FrameWrapper import GridFrame, ScrollGridFrame
from AirRowePy.GuiLibrary.Frames.EditableStringListFromCsvFileSubComps.ObjectListComponent import objectListComponent

#
class EditableStringListFromFileComponent(GridFrame):

    def __init__(self, parentFrame, headers):
        self.modalWindow = RootWindow("Hello World")
        mainFrame = window.getRoot()
        list = EditableStringListFromFileComponent(mainFrame, "ChargeList", fileName='chargeList.txt', fileRootPath=os.path.abspath('.'), fileDelimiter='\t', rangeEnd=0, rangeSize=4)
        window.show()
        self.listLabel = None
        if not type(grid) == {}.__class__:
            grid = {"r":0,"c":0}
        grid["px"]=10
        grid["py"]=10
        super().__init__(parentFrame, grid=grid)
        if fileRootPath:
            self.fileRootPath = fileRootPath
        else:
            self.fileRootPath = os.path.abspath(".")
        if fileName:
            self.fileName = fileName
        else:
            self.fileName = os.listdir(self.fileRootPath)
        if fileDelimiter:
            self.fileDelimiter = fileDelimiter
        else:
            self.fileDelimiter = "\t"
        self.fileDelimiter = fileDelimiter
        self.fileName = fileName
        self.listName = listName
        self.listContent = self.loadFile()
        self.listComponents = []
        listContentLen=len(self.listContent)
        if len(self.listContent) > 0:
            self.headers = self.listContent[0].keys()
        else:
            self.headers = []
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
        self.listFrameTopWrapper = MoreListComponent(self.scrollFrame, self.rangeStart, extendFunc=self.expand)
        self.listFrameBottomWrapper = MoreListComponent(self.scrollFrame, len(self.listContent)-self.rangeEnd-1, extendFunc=self.expand)
        self.optionsFrame = tkinter.Frame(self.frame, highlightbackground="black", highlightthickness=2)
        self.optionsFrame.grid(row=3,column=0,padx=10,pady=3)
        self.fullRefresh()

    def expand(self, amount, directionUp):
        if directionUp:
            for gridIdx, gListIdx in enumerate(range(self.rangeStart-amount, self.rangeStart,1)):
                #create element
                #prepend element
                component = objectListComponent(self.listFrame, self.listContent[gListIdx], gListIdx, self.headers, grid={"r":gridIdx, "c":0, "px":0, "py":0}, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit)
                self.listComponents.insert(0, component)
                self.scrollFrameWrapper.children.append(component)
            #fix gid of preexisting elements
            print(str(amount)+"- -"+str(self.rangeStart)+"-"+str(self.rangeEnd))
            for gridIdx in range(amount, len(self.listComponents), 1):
                self.listComponents[gridIdx].setIndexes(gridIdx=gridIdx)
            #adjust rangeStart
            self.rangeStart-=amount
        else:
            rangeGList = range(self.rangeEnd+1, self.rangeEnd+1+amount,1)
            rangeGrid = range(len(self.listComponents),len(self.listComponents)+amount)
            for gridIdx, gListIdx in zip(rangeGrid, rangeGList):
                #create element
                #append element
                component = objectListComponent(self.listFrame, self.listContent[gListIdx], gListIdx, self.headers, grid={"r":gridIdx, "c":0, "px":0, "py":0}, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit)
                self.listComponents.append(component)
                self.scrollFrameWrapper.children.append(component)

            #adjust rangeEnd
            self.rangeEnd+=amount

    def destroy(self):
        super().destroy()
        self.titleFrame.destroy()
        self.headerFrame.destroy()
        self.listFrameTopWrapper.destroy()
        self.listFrameBottomWrapper.destroy()
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

    def remove(self, gListRemIndex):
    #remove from master list
        self.listContent.pop(gListRemIndex)
        componentListRemoveIndex = gListRemIndex-self.rangeStart
    #remove from component list
        removedComponent = self.listComponents.pop(componentListRemoveIndex)
        moreElementsToRight = self.rangeEnd < len(self.listContent)-1
        #if shift from right
        if self.rangeStart <=0 or moreElementsToRight:
            gridRange=range(componentListRemoveIndex, len(self.listComponents), 1)
            globalListRange=range(gListRemIndex, self.rangeEnd+1, 1)
            #Update remaining component index info
            for gridIdx, gListIdx in zip(gridRange, globalListRange):
                self.listComponents[gridIdx].setIndexes(gridIdx=gridIdx, gListIdx=gListIdx)
            # attempt to add component from global list
            if moreElementsToRight:
                component = objectListComponent(self.listFrame, self.listContent[self.rangeEnd], self.rangeEnd, self.headers, grid={"r": len(self.listComponents) - 1, "c":0, "px":0, "py":0}, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit)
                self.listComponents.append(component)
                self.scrollFrameWrapper.children.append(component)
            #no more elements to fill range with. Decrease range size
            else:
                self.rangeEnd -= 1
        #if shift from left
        else: # fix grid layout of existing components
            if self.rangeStart > 0:
                self.rangeStart -= 1
                #insert new component with
                component = objectListComponent(self.listFrame, self.listContent[self.rangeStart], self.rangeStart, self.headers, grid={"r":0, "c":0, "px":0, "py":0}, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit)
                self.listComponents.insert(0, component)
                self.scrollFrameWrapper.children.append(component)
                gridRange=range(0, len(self.listComponents), 1)
                globalListRange=range(self.rangeStart, self.rangeEnd+1, 1)
            else:
                gridRange=range(componentListRemoveIndex, len(self.listComponents), 1)
                globalListRange=range(gListRemIndex, self.rangeEnd, 1)
            self.rangeEnd -= 1
            #update remaining component index info
            for gridIdx, gListIdx in zip(gridRange, globalListRange):
                self.listComponents[gridIdx].setIndexes(gridIdx=gridIdx, gListIdx=gListIdx)
        self.scrollFrameWrapper.children.remove(removedComponent)
        removedComponent.destroy()

    def add(self, insertIndex=-1, newEntry={}):
        print("BEGIN - start="+str(self.rangeStart)+"\tend="+str(self.rangeEnd)+"\tsize="+str(self.rangeEnd-self.rangeStart+1))
# INVALID INPUT and BASE CASE
        # print("start="+str(self.rangeStart)+"\tend="+str(self.rangeEnd))
        if insertIndex < self.rangeStart or insertIndex > self.rangeEnd+1:
            print("invalid insertIndex")
            return
        #create new component
        for header in self.headers:
            if not newEntry.__contains__(header):
                newEntry[header]=""
        newComponent = objectListComponent(self.listFrame, newEntry, insertIndex, self.headers, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit)
        #trivial case and invalid input
        compListInsertIdx = insertIndex - self.rangeStart
        # print("adding component at index "+str(insertIndex)+" and gridIndex "+str(compListInsertIdx))
        # print("compListInsertIdx ("+str(compListInsertIdx)+")>=("+str(len(self.listComponents))+") len(self.listComponents) or compListInsertIdx ("+str(compListInsertIdx)+")< 0")
        if compListInsertIdx >= len(self.listComponents) or compListInsertIdx < 0:
            self.listContent.append(newEntry)
            newComponent.setIndexes(gridIdx=len(self.listComponents))
            self.listComponents.append(newComponent)
            self.scrollFrameWrapper.children.append(newComponent)
            self.rangeEnd += 1
            print("TRIVIAL CASE =========================================================")
            return
# Determine Add Scenario
        #If start of displayed list is the start of the Master list, it stays that way.
        stickyStart = self.rangeStart==0
        #If end of displayed list is the end of the Master list, it stays that way.
        stickyEnd = self.rangeEnd==len(self.listContent)-1
        # determines which direction the components are shifted in the list to make room for the new component.
        shiftLeft = (((not stickyStart) and stickyEnd) and not (insertIndex == self.rangeStart)) or (not stickyStart and not stickyEnd)
        # if shiftLeft:
        #     print("shift Left")
        # else:
        #     print("shift Right")
            # print("StickyStart="+str(stickyStart))
            # print("StickyEnd="+str(stickyEnd))
            # print("rangeEnd="+str(self.rangeEnd)+", eol="+str(len(self.listContent)-1))
            # print("insertIndex="+str(insertIndex))
            # print("rangeStart="+str(self.rangeStart))
# Shift global list to make room for added component
        #make space for new component
        self.listContent.append({})
        #adjust master list
        for index in range(len(self.listContent)-1,insertIndex,-1):
            self.listContent[index] = self.listContent[index-1]

# Shift Component List to make room for added component


#adjust component grid alignment
        if shiftLeft:
            for gridIdx in range(compListInsertIdx, len(self.listComponents), 1):
                # print("old global list index "+str(self.listComponents[gridIdx].index)+"=>"+str(self.rangeStart+gridIdx+1)+"\t("+str(self.listComponents[gridIdx].content)+")")
                self.listComponents[gridIdx].setIndexes(gListIdx=self.rangeStart+gridIdx+1)
                # print("new global list index "+str(self.listComponents[gridIdx].index)+"=>"+str(self.rangeStart+gridIdx+1)+"\t("+str(self.listComponents[gridIdx].content)+")")

        #Determine shift Scenario
        incrament = 1 if shiftLeft else -1
        prevIdx = 0 if shiftLeft else self.rangeEnd-self.rangeStart
        currIdx = prevIdx+incrament
        # compListShiftTilltIdx = compListInsertIdx-incrament if shiftLeft else compListInsertIdx
        # increase list size if necessary
        if stickyStart and shiftLeft:
            self.listComponents.insert(0, self.listComponents[prevIdx])
            self.listComponents[prevIdx].setIndexes(gridIdx=0, gListIdx=self.rangeStart)
            prevIdx = currIdx
            currIdx += incrament
            print("Sticky start and shift left, so insert at start")
            self.rangeEnd += 1
        elif stickyEnd and not shiftLeft:
            print("Sticky end end shift right, so insert at end ("+str(prevIdx)+"/"+str(self.rangeEnd-self.rangeStart)+"/"+str(self.rangeEnd+1)+")")
            self.listComponents[prevIdx].setIndexes(gridIdx=prevIdx+1, gListIdx=self.rangeEnd+1)
            self.listComponents.append(self.listComponents[prevIdx])
            self.rangeEnd += 1
        else:
            print("Sticky start="+str(stickyStart))
            print("Sticky end="+str(stickyEnd))
            print("Destroying index=("+str(prevIdx)+"/"+str(prevIdx + self.rangeStart)+")")
            self.scrollFrameWrapper.children.remove(self.listComponents[prevIdx])
            self.listComponents[prevIdx].destroy()
            # self.listComponents.pop(prevIdx)
            #if shifting gid components toward 0 index to make room, adjust range indexes.
            if shiftLeft:
                self.rangeStart += 1
                self.rangeEnd += 1
                compListInsertIdx -= 1


        # for idx in range(0,len(self.listComponents),1):
        #     print("global list index "+str(self.listComponents[idx].index)+"\t("+str(self.listComponents[idx].content)+")\t-"+str(self.listComponents[idx].frame.grid_info()['row']))

        print(str(self.rangeStart+prevIdx)+"->"+"temp")
        shiftToIdx = compListInsertIdx
        print("compListInsertIdx="+str(compListInsertIdx)+"\tshiftToIdx="+str(shiftToIdx)+"\tprevIdx="+str(prevIdx))
        while prevIdx != shiftToIdx:
            print("prevIdx="+str(prevIdx)+"\tshiftToIdx="+str(shiftToIdx))
            print(str(self.listComponents[currIdx].index)+"->"+str(self.listComponents[prevIdx].index)+"\t"+str(currIdx)+"->"+str(prevIdx))
            self.listComponents[prevIdx] = self.listComponents[currIdx]
            self.listComponents[prevIdx].setIndexes(gridIdx=prevIdx, gListIdx=self.rangeStart+prevIdx if shiftLeft else self.rangeStart+prevIdx)
            prevIdx = currIdx
            currIdx += incrament
        print("prevIdx="+str(prevIdx)+"\tshiftToIdx="+str(shiftToIdx))
        self.listComponents[compListInsertIdx] = newComponent
        print("new"+"->"+str(self.rangeStart+compListInsertIdx))
        newComponent.setIndexes(gridIdx=compListInsertIdx)
        self.scrollFrameWrapper.children.append(newComponent)
        self.listContent[insertIndex] = newEntry
        # print("start="+str(self.rangeStart)+"\tend="+str(self.rangeEnd)+"\n\n")


        # for idx in range(len(self.listComponents)-3,len(self.listComponents),1):
        #     print("global list index "+str(self.listComponents[idx].index)+"\t("+str(self.listComponents[idx].content)+")")

        print("component-list-size="+str(len(self.listComponents)))
        for component in self.listComponents:
            print(component.content)
        print("start="+str(self.rangeStart)+"\tend="+str(self.rangeEnd)+"\tsize="+str(self.rangeEnd-self.rangeStart+1))


        # for idx in range(0,len(self.listComponents),1):
        #     print("global list index "+str(self.listComponents[idx].index)+"\t("+str(self.listComponents[idx].content)+")\t-"+str(self.listComponents[idx].frame.grid_info()['row']))
        print("\n\n\n")


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
        #delete children
        for child in self.children:
            child.destroy()
        for child in self.scrollFrameWrapper.children:
            child.destroy()
        self.children = []
        self.listComponents=[]
        if self.listLabel:
            self.listLabel.destroy()

        self.listLabel = tkinter.Label(self.titleFrame, text=self.listName)
        self.listLabel.grid(row=0,column=0,padx=10,pady=20)
        for idx, header in enumerate(self.headers):
            print(str(idx)+" - "+header)
            headerLabel = tkinter.Label(self.headerFrame, text=header, width=17, anchor="w", borderwidth=1, relief="groove")
            headerLabel.grid(row=0,column=idx,padx=(2,0),pady=0)
            self.children.append(headerLabel)
        idx = len(self.headers)
        loadButton = tkinter.Button(self.headerFrame, text="Load", command=self.reloadFromFile)
        loadButton.grid(row=0,column=idx,padx=(5,0),pady=0)
        idx+=1
        saveButton = tkinter.Button(self.headerFrame, text="Save", command=self.saveToFile)
        saveButton.grid(row=0,column=idx,padx=(5,0),pady=0)


        self.children.append(self.listLabel)
        #create new children
        # for idx, content in enumerate(self.listContent):
        # print("contents")
        # print(self.listContent)
        # print(" ------- "+str(self.rangeStart)+"-"+str(self.rangeEnd)+" ------- ")
        for gridIdx, gListIdx in enumerate(range(self.rangeStart, self.rangeEnd+1, 1)):
            #create children components
            label = objectListComponent(self.listFrame, self.listContent[gListIdx], gListIdx, self.headers, grid={"r":gridIdx, "c":0, "px":0, "py":0}, addComponent=self.add, removeComponent=self.remove, updateComponent=self.edit)
            self.listComponents.append(label)
            self.scrollFrameWrapper.children.append(label)
        # print("components")
        # print(self.listComponents)
    def reloadFromFile(self):
        self.listContent = self.loadFile()
        self.fullRefresh()
        print("file loaded")
    def saveToFile(self):
        self.saveFile(self.listContent)
        print("file saved")
    def loadFile(self):
        with open(os.path.join(self.fileRootPath, self.fileName), 'r') as datasource_file:
            return list(csv.DictReader(datasource_file, delimiter=self.fileDelimiter))

    def saveFile(self, listContents):
        with open(os.path.join(self.fileRootPath, self.fileName), 'w', newline='') as datasource_file:
            writer = csv.DictWriter(datasource_file, fieldnames=self.headers, delimiter=self.fileDelimiter)
            writer.writeheader()
            writer.writerows(listContents)

