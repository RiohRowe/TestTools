import tkinter

from AirRowePy.GuiLibrary.Frames.FrameWrapper import GridFrame

VAR='v'
COMPONENT='C'
TRACES = 'T'
SHOW_MORE = 'M'
SHOW_LESS = 'L'
SHOW_LEAST = 'N'
SHOW_ALL = 'A'

BUTTON_STATE = "state"
ENABLED_STATE = "normal"
DISABLED_STATE = "disabled"

class ListExpandOptionsComponent(GridFrame):
    def __init__(self, parent, numberHiddenElements, expandDirDown, adjustHiddenFunc, getNumShownFunc, showMoreIndicator=None, showLessIndicator=None, incrament=10, grid=None):
        if not grid:
            grid={"r":0,"c":0,"px":0,"py":0}
        self.numHidden = numberHiddenElements
        self.smInd=showMoreIndicator if showMoreIndicator else ('v' if expandDirDown else '^')
        self.slInd=showLessIndicator if showLessIndicator else ('^' if expandDirDown else 'v')
        self.expandDirDown = expandDirDown
        self.incrament = incrament
        self.adjustHiddenFunc = adjustHiddenFunc
        self.getNumDispl = getNumShownFunc
        self.buttonComps = {}
        self.countLabelComps = {}
        super().__init__(parent, grid)
        self.render()

    def hideExpand(self):
        self.countLabelComps[COMPONENT].grid_remove()
        self.buttonComps[SHOW_MORE][BUTTON_STATE]=DISABLED_STATE
        self.buttonComps[SHOW_ALL][BUTTON_STATE]=DISABLED_STATE
        self.expandHidden=True
    def showExpand(self):
        self.countLabelComps[COMPONENT].grid()
        self.buttonComps[SHOW_MORE][BUTTON_STATE]=ENABLED_STATE
        self.buttonComps[SHOW_ALL][BUTTON_STATE]=ENABLED_STATE
        self.expandHidden=False
    def hideShrink(self):
        self.buttonComps[SHOW_LESS][BUTTON_STATE]=DISABLED_STATE
        self.buttonComps[SHOW_LEAST][BUTTON_STATE]=DISABLED_STATE
        self.shrinkHidden=True
    def showShrink(self):
        self.buttonComps[SHOW_LESS][BUTTON_STATE]=ENABLED_STATE
        self.buttonComps[SHOW_LEAST][BUTTON_STATE]=ENABLED_STATE
        self.shrinkHidden=False

    def showMore(self, all=False):
        if self.numHidden <= self.incrament or all:
            self.adjustHiddenFunc(self.numHidden, self.expandDirDown)
            self.numHidden = 0
        else:
            self.adjustHiddenFunc(self.incrament, self.expandDirDown)
            self.numHidden -= self.incrament
            self.countLabelComps[VAR].set("..."+str(self.numHidden))
    def showAll(self):
        self.showMore(all=True)
    def showLess(self, all=False):
        maxHide = self.getNumDispl()-1
        if maxHide <= self.incrament or all:
            self.adjustHiddenFunc(-maxHide, self.expandDirDown)
            self.numHidden+=maxHide
        else:
            self.adjustHiddenFunc( -self.incrament, self.expandDirDown)
            self.numHidden+=self.incrament
        self.countLabelComps[VAR].set("..."+str(self.numHidden))
    def showLeast(self):
        self.showLess(all=True)

    def setNumHidden(self,num):
        self.numHidden = num
        self.countLabelComps[VAR].set("..."+str(self.numHidden))

    def render(self):
        numDisplayed = self.getNumDispl()
        self.expandHidden = self.numHidden==0
        self.shrinkHidden = numDisplayed==1
        idx=0
        self.countLabelComps[VAR] = tkinter.StringVar(value="..."+str(self.numHidden))
        self.countLabelComps[COMPONENT] = tkinter.Label(self.frame, textvariable=self.countLabelComps[VAR])
        self.countLabelComps[COMPONENT].grid(row=0,column=idx,padx=0,pady=0,sticky="nsew")
        if self.numHidden == 0:
            self.countLabelComps[COMPONENT].grid_remove()
        idx+=1

        showMoreButton = tkinter.Button(self.frame, text=self.smInd, command=self.showMore, state=DISABLED_STATE if self.numHidden==0 else ENABLED_STATE)
        showMoreButton.grid(row=0,column=idx,padx=0,pady=0)
        self.buttonComps[SHOW_MORE] = showMoreButton
        idx+=1

        showAllButton = tkinter.Button(self.frame, text=self.smInd+self.smInd, command=self.showAll, state=DISABLED_STATE if self.numHidden==0 else ENABLED_STATE)
        showAllButton.grid(row=0,column=idx,padx=0,pady=0)
        self.buttonComps[SHOW_ALL] = showAllButton
        idx+=1

        showlessButton = tkinter.Button(self.frame, text=self.slInd, command=self.showLess, state=DISABLED_STATE if numDisplayed<=1 else ENABLED_STATE)
        showlessButton.grid(row=0,column=idx,padx=0,pady=0)
        self.buttonComps[SHOW_ALL] = showlessButton
        idx+=1

        showLeastButton = tkinter.Button(self.frame, text=self.slInd+self.slInd, command=self.showLeast, state=DISABLED_STATE if numDisplayed<=1 else ENABLED_STATE)
        showLeastButton.grid(row=0,column=idx,padx=0,pady=0)
        self.buttonComps[SHOW_ALL] = showLeastButton
        idx+=1

        self.buttonComps = {
            SHOW_MORE: showMoreButton,
            SHOW_ALL: showAllButton,
            SHOW_LESS: showlessButton,
            SHOW_LEAST: showLeastButton
        }