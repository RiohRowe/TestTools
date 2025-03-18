import tkinter.ttk
from math import ceil

from AirRowePy.GuiLibrary.FileManager import FileManager
from AirRowePy.GuiLibrary.Frames.FrameWrapper import GridFrame, ScrollPackFrame
from AirRowePy.GuiLibrary.ModalFrames.modalModules.EditCategoryFileModule import SCROLL, INNER_FRAME
from AirRowePy.GuiLibrary.StringCompareUtil import StringCompareUtil

# entry structure:
    #{
    #    "key1": None,
    #    "key2": None
    #}
HEADERS='H'
BODY='B'
BUTTONS='b'
VAR='V'
COMPONENT='C'
KEY_LB='K'
VALUE_TB='v'
VALUE_LB="vl"
SUGGESTION_BT="SB"
FRAME='F'
TRACES='T'
RESOLVE_BT='R'
SCROLL='s'
INNER_FRAME='I'
OUTTER_FRAME='o'
NONE = None

SELECT_SUGGESTIONS_DD="SD"
SELECT_SUGGESTION_LB = "SL"
SCORE = "S"

ORIGINAL = 'O'
ALPHA_SORTED = 'A'


bgColor1 = "#FFFFEE"
bgColor2 = "#FFFFAD"

keyWidth = 60
valueWidth = 60
suggestionWidth = 60


class AssignValuesToMapModal(GridFrame):
    def __init__(self, parent,resolve,
                 elements=[{"apple":"oranges","peas":"carrots"}],
                 otherOptions={},
                 grid={"r": 0, "c": 0, "px": 0, "py": 0}) -> None:
        super().__init__(parent, grid=grid)
        self.elements = elements
        print("elements1=\n"+str(self.elements)+"\n\n")
        self.valueBreakdowns={}
        self.resolve = resolve
        self.strCompUtil = StringCompareUtil()
        self.suggestionPool = []
        self.formComps={}
        self.fm = FileManager(FileManager.CATEGORY_FILES_PATH)
        self.render()

    def updateSuggestion(self, key):
        self.elements[key] = self.formComps[BODY][key][VALUE_TB][VAR].get()
        if(self.elements[key] == ""):
            self.valueBreakdowns[key] = self.breakdownWord(key)
        else:
            self.valueBreakdowns[key] = self.breakdownWord(self.elements[key])
        print("updating key"+str(key)+" suggestion using value "+self.formComps[BODY][key][VALUE_TB][VAR].get())
        self.formComps[BODY][key][SUGGESTION_BT][VAR].set(self.makeSuggestion(key))

    def getValues(self):
        return self.elements

    def handleApplySuggestion(self, key):
        self.formComps[BODY][key][VALUE_TB][VAR].set(self.formComps[BODY][key][SUGGESTION_BT][VAR].get())

    def breakdownWord(self, string):
        word = {
            ORIGINAL:string,
            ALPHA_SORTED:self.alphaSort(string)
        }
        return word

    def alphaSort(self, string):
        if len(string) == 1:
            return string.lower()
        midIdx = ceil(len(string)/2)
        sub1 = self.alphaSort(string[0:midIdx])
        sub2 = self.alphaSort(string[midIdx:])
        sub1Idx = 0
        sub2Idx = 0
        sortedStr = ""
        for Idx in range(0, len(string)):
            if sub1Idx >= len(sub1):
                return sortedStr+sub2[sub2Idx:]
            elif sub2Idx >= len(sub2):
                return sortedStr+sub1[sub1Idx:]
            elif sub1[sub1Idx] > sub2[sub2Idx]:
                sortedStr+=sub2[sub2Idx]
                sub2Idx+=1
            else:
                sortedStr+=sub1[sub1Idx]
                sub1Idx+=1

    def updateSuggestionPoolComponents(self):
        oldSize = len(self.suggestionComps[SELECT_SUGGESTION_LB])
        newSize = len(self.suggestionPool)
        if oldSize >= newSize: #update existing
            for idx in range(0,newSize):
                self.suggestionComps[SELECT_SUGGESTION_LB][idx][VAR].set(self.suggestionPool[idx][ORIGINAL])
            if oldSize > newSize: # delete excess
                for idx in range(oldSize,newSize):
                    self.suggestionComps[SELECT_SUGGESTION_LB][idx][COMPONENT].destroy()
        else:
            for idx in range(0,oldSize):
                self.suggestionComps[SELECT_SUGGESTION_LB][idx][VAR].set(self.suggestionPool[idx][ORIGINAL])
            for idx in range(oldSize,newSize):
                suggestionComps = {}
                suggestionComps[VAR] = tkinter.StringVar(value=self.suggestionPool[idx][ORIGINAL])
                suggestionComps[COMPONENT] = tkinter.Label(self.suggestionComps[SCROLL][INNER_FRAME], textvariable=suggestionComps[VAR])
                suggestionComps[COMPONENT].grid(row=idx+1,column=0,padx=0,pady=0,sticky="nsew")
                self.suggestionComps[SELECT_SUGGESTION_LB].append(suggestionComps)



    def handleSelectSuggestionsFile(self, *args):
        selectedFile = args[0]
        # selectedFile = self.suggestionComps[SELECT_SUGGESTIONS_DD][VAR].get()
        #updateSuggestValueList
        if selectedFile == NONE:
            self.suggestionPool = []
            for suggestion in self.formComps[BODY][SUGGESTION_BT]:
                suggestion[COMPONENT].destroy()
            return
        suggestions = self.fm.readFileToList(selectedFile, bodyOnly=True)
        uniqueSuggestions = []
        for word in suggestions:
            if not uniqueSuggestions.__contains__(word):
                uniqueSuggestions.append(word)
        self.suggestionPool = self.objListSort([self.breakdownWord(word) for word in uniqueSuggestions],[ALPHA_SORTED])
        #updateSuggestionPool
        self.updateSuggestionPoolComponents()
        #updateSuggestions
        for key, tableComps in self.formComps[BODY].items():
            tableComps[SUGGESTION_BT][VAR].set(self.makeSuggestion(key))

    def makeSuggestion(self, key, default="DEFAULT_SUGGESTION"):
        valueBreakdown = self.valueBreakdowns[key]
        for compBreakdown in self.suggestionPool:
            containsCharsScore=self.strCompUtil.rankAlphaWordComparison(self.strCompUtil.compareAlphaWords(valueBreakdown[ALPHA_SORTED], compBreakdown[ALPHA_SORTED]))
            subStrScore=0
            compBreakdown[SCORE]= subStrScore+containsCharsScore
        rankedSuggestions = self.objListSort(self.suggestionPool, [SCORE], False)
        # print("RANK:")
        # for idx in range(0,5 if len(rankedSuggestions)>4 else len(rankedSuggestions)):
        #     print(rankedSuggestions[idx][ORIGINAL]+" - "+str(rankedSuggestions[idx][SCORE]))
        # print("")
        if len(rankedSuggestions) == 0:
            return self.breakdownWord(default)[ORIGINAL]
        return rankedSuggestions[0][ORIGINAL]
    def render(self):
        self.tableFrame = tkinter.Frame(self.frame)
        self.tableFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.suggestionsFrame = tkinter.Frame(self.frame)
        self.suggestionsFrame.grid(row=0,column=1,padx=0,pady=0,sticky="nsew")
        #labels
        self.formComps[HEADERS] = {
            KEY_LB:{},
            VALUE_LB:{},
            SUGGESTION_BT:{}
        }
        self.formComps[HEADERS][KEY_LB][FRAME] = tkinter.Frame(self.tableFrame, background=bgColor1)
        self.formComps[HEADERS][KEY_LB][FRAME].grid(row=0,column=0,padx=0,pady=0,sticky="nsew")
        self.formComps[HEADERS][KEY_LB][VAR] = tkinter.StringVar(value="ORIGINAL_VAL")
        self.formComps[HEADERS][KEY_LB][COMPONENT] = tkinter.Label(self.formComps[HEADERS][KEY_LB][FRAME], textvariable=self.formComps[HEADERS][KEY_LB][VAR])
        self.formComps[HEADERS][KEY_LB][COMPONENT].grid(row=0,column=0,padx=0,pady=0,sticky="nsew")
        self.formComps[HEADERS][VALUE_LB][FRAME] = tkinter.Frame(self.tableFrame, background=bgColor1)
        self.formComps[HEADERS][VALUE_LB][FRAME].grid(row=0,column=1,padx=0,pady=0,sticky="nsew")
        self.formComps[HEADERS][VALUE_LB][VAR] = tkinter.StringVar(value="MAPPED_VAL")
        self.formComps[HEADERS][VALUE_LB][COMPONENT] = tkinter.Label(self.formComps[HEADERS][VALUE_LB][FRAME], textvariable=self.formComps[HEADERS][VALUE_LB][VAR])
        self.formComps[HEADERS][VALUE_LB][COMPONENT].grid(row=0,column=0,padx=0,pady=0,sticky="nsew")
        self.formComps[HEADERS][SUGGESTION_BT][FRAME] = tkinter.Frame(self.tableFrame, background=bgColor1)
        self.formComps[HEADERS][SUGGESTION_BT][FRAME].grid(row=0,column=2,padx=0,pady=0,sticky="nsew")
        self.formComps[HEADERS][SUGGESTION_BT][VAR] = tkinter.StringVar(value="SUGGESTED_VAL")
        self.formComps[HEADERS][SUGGESTION_BT][COMPONENT] = tkinter.Label(self.formComps[HEADERS][SUGGESTION_BT][FRAME], textvariable=self.formComps[HEADERS][SUGGESTION_BT][VAR])
        self.formComps[HEADERS][SUGGESTION_BT][COMPONENT].grid(row=0,column=0,padx=0,pady=0,sticky="nsew")
        self.formComps[BODY]={}

        for idx, key in enumerate(self.elements.keys()):
            value = self.elements[key]
            entry = {
                KEY_LB:{},
                VALUE_TB:{},
                SUGGESTION_BT:{}
            }

            self.valueBreakdowns[key]=self.breakdownWord(key)
            print("row-"+str(idx)+"- key:("+str(key)+")value:("+str(value)+")")
            entry[KEY_LB][FRAME] = tkinter.Frame(self.tableFrame, background=bgColor1 if idx % 2 == 0 else bgColor2)
            entry[KEY_LB][FRAME].grid(row=idx+1,column=0,padx=0,pady=0,sticky="nsew")
            entry[KEY_LB][VAR]=tkinter.StringVar(value=key)
            entry[KEY_LB][COMPONENT] = tkinter.Label(entry[KEY_LB][FRAME], textvariable=entry[KEY_LB][VAR])
            entry[KEY_LB][COMPONENT].grid(row=0,column=0,padx=0,pady=0,sticky="nsew")

            entry[VALUE_TB][FRAME] = tkinter.Frame(self.tableFrame, background=bgColor1 if idx % 2 == 0 else bgColor2)
            entry[VALUE_TB][FRAME].grid(row=idx+1,column=1,padx=0,pady=0,sticky="nsew")
            entry[VALUE_TB][VAR]=tkinter.StringVar(value=value)
            entry[VALUE_TB][COMPONENT] = tkinter.Entry(entry[VALUE_TB][FRAME], textvariable=entry[VALUE_TB][VAR])
            entry[VALUE_TB][COMPONENT].grid(row=0, column=1, padx=3, pady=5, sticky="nsew")
            entry[VALUE_TB][TRACES] = []
            entry[VALUE_TB][TRACES].append(entry[VALUE_TB][VAR].trace_add("write", lambda *args, k=key: self.updateSuggestion(k)))

            entry[SUGGESTION_BT][FRAME] = tkinter.Frame(self.tableFrame, background=bgColor1 if idx % 2 == 0 else bgColor2)
            entry[SUGGESTION_BT][FRAME].grid(row=idx+1,column=2,padx=0,pady=0,sticky="nsew")
            entry[SUGGESTION_BT][VAR]=tkinter.StringVar(value=self.makeSuggestion(key))
            entry[SUGGESTION_BT][COMPONENT] = tkinter.Button(entry[SUGGESTION_BT][FRAME], textvariable=entry[SUGGESTION_BT][VAR], command=lambda *args, k=key: self.handleApplySuggestion(k))
            entry[SUGGESTION_BT][COMPONENT].grid(row=0,column=2,padx=0,pady=0,sticky="nsew")
            self.formComps[BODY][key] = entry

        self.formComps[BUTTONS]={}
        self.formComps[BUTTONS][RESOLVE_BT]=tkinter.Button(self.frame, text="RESOLVE", command=self.resolve)
        self.formComps[BUTTONS][RESOLVE_BT].grid(row=2,column=0,padx=0,pady=0,sticky="nsew",columnspan=2)

        #Setup suggestions
        self.suggestionComps = {
            SELECT_SUGGESTIONS_DD:{},
            SCROLL:{},
            SELECT_SUGGESTION_LB:[]
        }
        self.suggestionComps[SELECT_SUGGESTIONS_DD][VAR] = tkinter.StringVar(value=NONE)
        self.suggestionComps[SELECT_SUGGESTIONS_DD][COMPONENT] = tkinter.ttk.OptionMenu(self.suggestionsFrame, self.suggestionComps[SELECT_SUGGESTIONS_DD][VAR], "NONE", *["NONE",*self.fm.getFilesNoExt()], command=self.handleSelectSuggestionsFile)
        self.suggestionComps[SELECT_SUGGESTIONS_DD][COMPONENT].grid(row=0,column=0,padx=0,pady=0,sticky="nsew")
        
        self.suggestionComps[SCROLL][OUTTER_FRAME]=tkinter.Frame(self.suggestionsFrame)
        self.suggestionComps[SCROLL][COMPONENT]=ScrollPackFrame(self.suggestionComps[SCROLL][OUTTER_FRAME],height=500, width=125)
        self.suggestionComps[SCROLL][INNER_FRAME] = self.suggestionComps[SCROLL][COMPONENT].getInnerFrame()
        self.suggestionComps[SCROLL][OUTTER_FRAME].grid(row=1,column=0,padx=0,pady=0,sticky="nsew")
        rIdx = 0
        for wordMeta in self.suggestionPool:
            suggestionComps = {}
            suggestionComps[VAR] = tkinter.StringVar(value=wordMeta[ORIGINAL])
            suggestionComps[COMPONENT] = tkinter.Label(self.suggestionComps[SCROLL][INNER_FRAME], textvariable=suggestionComps[VAR])
            suggestionComps[COMPONENT].grid(row=rIdx,column=0,padx=0,pady=0,sticky="nsew")
            rIdx += 1
            self.suggestionComps[SELECT_SUGGESTION_LB].append(suggestionComps)

    def getValues(self):
        retVal = {}
        for key,value in self.formComps[BODY].items():
            retVal[key]=value[VALUE_TB][VAR].get()
        return retVal
    # # remove component
    def destroy(self):
        #remove traces
        for key, comps in self.formComps[BODY].items():
            for trace in comps[VALUE_TB][TRACES]:
                comps[VALUE_TB][VAR].trace_remove("write", trace)
            comps[VALUE_TB][TRACES] = []
        #destroy root component (recursively destroys components)
        super().destroy()
    # # change relative position reference. Used by show method.
    # def update(self, newPos):
    #     for key in self.grid:
    #         if key in newPos:
    #             self.grid[key] = newPos[key]
    #     if self.frame.grid_info():
    #         self.show()

    def insertSortObj(self, objList, item, keyChain, asc):
        for sItemIdx in range(0, len(objList)):
            if asc and self.getNestedVal(objList[sItemIdx],keyChain) > self.getNestedVal(item, keyChain):
                objList.insert(sItemIdx, item)
                return
            elif not asc and self.getNestedVal(objList[sItemIdx],keyChain) < self.getNestedVal(item, keyChain):
                objList.insert(sItemIdx, item)
                return
        objList.append(item)
    def getNestedVal(self, item, keyChain):
        for key in keyChain:
            item = item[key]
        return item
    def objListSort(self, list, keyChain, asc=True):
        newList=[]
        for item in list:
            self.insertSortObj(newList,item,keyChain, asc=asc)
        return newList