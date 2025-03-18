import tkinter
from tkinter import ttk

from AirRowePy.GuiLibrary.FileManager import FileManager
from AirRowePy.GuiLibrary.Frames.FrameWrapper import GridFrame
from AirRowePy.GuiLibrary.ModalFrames.ModalWrapper import ModalWrapper
from AirRowePy.GuiLibrary.ModalFrames.WigitFactory import WigitFactory
from AirRowePy.GuiLibrary.ModalFrames.modalModules.AddToListModalComponents.AssignValuesModal.AssignValuesToMapModal import \
    AssignValuesToMapModal
from AirRowePy.GuiLibrary.ModalFrames.modalModules.EditCategoryFileModule import FILE_MANAGER, FILE_NAME, FILE_EXT, \
    EditCategoryFileModule

TITLE_LB = "H"
PARSER_TB = "PT"
BUILDER_TB = "BT"
SAMPLE_IN_TB = "SI"
SAMPLE_OUT_LB = "SO"
VAR = "VA"
COMPONENT = "C"
DEFAULT_VALUE = "defaultValue"
EDITABLE = "editable"
TRACE_ADD = "TA"
TRACE_REMOVE = "TR"
SET_DISABLE = "SD"
ENABLE_HEADER_CB = "EC"
CUSTOM_VALUE_MAP_DD = "VD"
CUSTOM_CATEGORY_MAP_DD = "CD"
FRAME = "F"
SHIFT_LEFT_BT = "L"
SHIFT_RIGHT_BT = "R"

DESTROY = "D"
GET_VALUE = "GV"
SET_VALUE = "SV"
TRACES = "T"
MAP = "M"
MAPPING_DEFAULT = "MD"
GRID_CONFIGURE = "GC"

REGEX_TRANSLATION_TYPE = "R"
DIRECT_MAP_TRANSLATION_TYPE = "DM"

defaultSpaceX=10
defaultSpaceY=5
TABLE_CELL_WIDTH=100
TABLE_CELL_HEIGHT=30
bgColor1 = "#FFFFEE"
bgColor2 = "#FFFFAD"

PARSER = "P"
BUILDER = "B"
NONE = "NONE"

wigitFactory = WigitFactory()

class RowTranslatorTableFrame(GridFrame):
    #Translations format:
    #{
    #   "headerName1":{
    #       "P":"regex to isolate incoming data",
    #       "B":"regex to specify outgoing data format"
    #       "M":"obj with key-value pair mapping"
    #       "MD":"default value when mapping does not exist for value"
    #   }
    #}
    # elements structure:
    #[
    #   {
    #       Header1: {
    #           "type": var type (EX: "t"-text, "n"-number, "dymd"-dateYearMonthDay)
    #           "editable": allow editing of value? (EX: True, False)
    #           "defaultValue": starting value (EX: "HelloWorld", 1, 2025/1/24)
    #           "getVal": function for getting the current value
    #           "setVal": function for setting the value
    #           "TA": function for adding traces
    #           "TR": function for removing traces
    #           "T": array of traces
    #           "destroy": function for deleting the wigit
    #       },
    #       Header2: {...},
    #       Header3: {...},
    #       Header4: {...}
    #   }
    #]
    def __init__(self, parent, elements, numElements, resolve, updateHeaders, translations={}, grid={"r":0, "c":0, "px":0, "py":0}):
        super().__init__(parent, grid)
        self.translaterFrame = tkinter.Frame(self.frame)
        self.translaterFrame.grid(row=0, column=0)
        self.tableFrame = tkinter.Frame(self.frame)
        self.tableFrame.grid(row=1, column=0)
        self.buttonsFrame = tkinter.Frame(self.frame)
        self.buttonsFrame.grid(row=2, column=0, pady=3)

        self.resolve = resolve
        self.updateHeaders=updateHeaders

        self.numHidden = numElements-len(elements)
        self.headerOrder = list(elements[0].keys()) if len(elements) > 0 else []
        self.numClippedRowsLabel = {}

        self.elements = elements
        self.translations = translations
        self.categoryMaps={}
        for header in self.headerOrder:
            self.categoryMaps[header] = None
            if self.translations.__contains__(header):
                if not self.translations[header].__contains__(PARSER):
                    self.translations[header][PARSER] = ""
                if not self.translations[header].__contains__(BUILDER):
                    self.translations[header][BUILDER] = ""
                if not self.translations[header].__contains__(MAP):
                    self.translations[header][MAP] = None
                if not self.translations[header].__contains__(MAPPING_DEFAULT):
                    self.translations[header][MAPPING_DEFAULT] = NONE
            else:
                self.translations[header] = {PARSER:"",BUILDER:"",MAP:None,MAPPING_DEFAULT:NONE}

        #[{
        #   TITLE_LB:{
        #       VAR: header-1-labelValueVariable,
        #       COMPONENT: header-1-label
        #   },
        #   PARSER_TB:{
        #       VAR: header-1-InputRegexValueVariable,
        #       COMPONENT: header-1-InputRegexTextField
        #       TRACES: []
        #   },
        #   BUILDER_TB:{
        #       VAR: header-1-OutputRegexValueVariable,
        #       COMPONENT: header-1-OutputRegexTextField
        #       TRACES: []
        #   },
        #   SAMPLE_IN_TB:{
        #       VAR: header-1-SampleInputValueVariable,
        #       COMPONENT: header-1-SampleInputTextField
        #       TRACES: []
        #   },
        #   SAMPLE_OUT_LB:{
        #       VAR: header-1-SampleOutputValueVariable,
        #       COMPONENT: header-1-SampleOutputLabel
        #   }
        # }, ...]
        self.transTableComps = []
        self.tableHeaderLabelComps = []
        self.vMapFM = FileManager(FileManager.TRANSLATION_MAP_FILES_PATH)
        self.cMapFM = FileManager(FileManager.CATEGORY_FILES_PATH)
        self.render()
    def addMap(self, header):
        emptyRowMap = {}
        print("HEADER="+header)
        for row in self.getValues():
            emptyRowMap[row[header]]=""
        fileName = header+"mapFile"
        modal = ModalWrapper(AssignValuesToMapModal, "AddMapModal", elements=emptyRowMap, handleResolveValue=lambda *args, fn=fileName, value={}: self.vMapFM.writeMapToFile(fn, value)),
    def editMap(self,fileName):
        rowMap = self.vMapFM.readFileToMap(fileName)
        modal = ModalWrapper(AssignValuesToMapModal, "EditMapModal", elements=rowMap, handleResolveValue=lambda *args, fn=fileName, value={}: self.vMapFM.writeMapToFile(fn, value)),

    def updateTransitions(self, header, parserStr=None, builderStr=None):
        idx = self.headerOrder.index(header)
        if not parserStr == None:
            self.translations[header][PARSER] = self.transTableComps[idx][PARSER_TB][VAR].get()
        if not builderStr == None:
            self.translations[header][BUILDER] = self.transTableComps[idx][BUILDER_TB][VAR].get()
        # update transTable
            idx=self.headerOrder.index(header)
            self.transTableComps[idx][SAMPLE_OUT_LB][VAR].set(self.translateRegxInOut(self.translations[header][PARSER], self.translations[header][BUILDER], self.transTableComps[idx][SAMPLE_IN_TB][VAR].get()))
        # update table
        for element in self.elements:
            element[header][SAMPLE_OUT_LB][VAR].set(self.translateRegxInOut(self.translations[header][PARSER], self.translations[header][BUILDER], element[header][GET_VALUE]()))

    def updateTransitionSampleInput(self, header):
        idx=self.headerOrder.index(header)
        self.transTableComps[idx][SAMPLE_OUT_LB][VAR].set(self.translateRegxInOut(self.translations[header][PARSER], self.translations[header][BUILDER], self.transTableComps[idx][SAMPLE_IN_TB][VAR].get()))

    def updateTableOutput(self, idx, header):
        translation = self.translations[header]
        cell  = self.elements[idx][header]
        cell[SAMPLE_OUT_LB][VAR].set(self.translateRegxInOut(translation[PARSER], translation[BUILDER], cell[GET_VALUE]()))

    def updateTableInput(self, idx, header):
        self.elements[idx][header][DEFAULT_VALUE]=self.elements[idx][header][GET_VALUE]()
        self.elements[idx][header][VAR].set(self.elements[idx][header][DEFAULT_VALUE])
    def toggleHeaderEnabled(self, idx):
        if len(self.transTableComps) > idx:
            #disable
            if self.transTableComps[idx][ENABLE_HEADER_CB][VAR].get():
                for row in self.elements:
                    row[self.headerOrder[idx]][SET_DISABLE](disabled=True)
            else:
                for row in self.elements:
                    cell = row[self.headerOrder[idx]]
                    cell[SET_DISABLE](disabled= not cell[EDITABLE])
    def countUnmapped(self, idx):
        return len(self.getUnMappedStrings(idx))
    def getUnMappedStrings(self, idx):
        unmappedStrings = []
        headerName = self.headerOrder[idx]
        map = self.translations[headerName][MAP]
        if map == None:
            return unmappedStrings
        else:
            for row in self.elements:
                val = row[headerName][GET_VALUE]()
                if not (map.__contains__(val) or unmappedStrings.__contains__(val)):
                    unmappedStrings.append(val)
        return unmappedStrings
    def transMapUpdateDefault(self, idx):
        #get Default
        default = self.transTableComps[idx][BUILDER_TB][VAR].get()
        headerName = self.headerOrder[idx]
        self.translations[headerName][MAPPING_DEFAULT] = default
        #apply Default
        #translations
        if not self.translations[headerName][MAP].__contains__(self.transTableComps[idx][SAMPLE_IN_TB][VAR].get()):
            self.transTableComps[idx][SAMPLE_OUT_LB][VAR].set(default)
        #table
        for row in self.elements:
            if not self.translations[headerName][MAP].__contains__(row[headerName][GET_VALUE]()):
                row[headerName][SAMPLE_OUT_LB][VAR].set(default)


    def selectCategoryType(self, idx):
        print("selecting category mapping")
        header = self.headerOrder[idx]
        fileName = self.transTableComps[idx][CUSTOM_CATEGORY_MAP_DD][VAR].get()
        # normal
        if fileName == NONE:
            print("no category map")
            self.categoryMaps[header] == None
        else:
            print("new translation map file selected:"+fileName)
            self.categoryMaps[header]={
                FILE_MANAGER:self.cMapFM,
                FILE_NAME:fileName,
                FILE_EXT:None
            }
    def selectTranslationType(self, idx):
        headerName = self.headerOrder[idx]
        print("selecting translation mapping")
        fileName = self.transTableComps[idx][CUSTOM_VALUE_MAP_DD][VAR].get()
        # normal
        if fileName == NONE:
            print("no translation map")
            if self.translations[headerName][MAP] == None:
                return
            else:
                self.translations[headerName][MAP] = None
                # replace existing traces
                    #translator
                self.removeTracesTransTable(idx)
                self.transTableComps[idx][PARSER_TB][COMPONENT].configure(state='normal')
                self.transTableComps[idx][PARSER_TB][VAR].set(self.translations[headerName][PARSER])
                self.transTableComps[idx][BUILDER_TB][VAR].set(self.translations[headerName][BUILDER])
                self.transTableComps[idx][SAMPLE_OUT_LB][VAR].set(self.translateRegxInOut(self.transTableComps[idx][PARSER_TB][VAR].get(), self.transTableComps[idx][BUILDER_TB][VAR].get(), self.transTableComps[idx][SAMPLE_IN_TB][VAR].get()))
                self.setTracesTransTable(REGEX_TRANSLATION_TYPE, idx)
                    #table
                self.removeTracesElementTable(idx)
                for rIdx, row in enumerate(self.elements):
                    row[headerName][SAMPLE_OUT_LB][VAR].set(self.translateRegxInOut(self.transTableComps[idx][PARSER_TB][VAR].get(), self.transTableComps[idx][BUILDER_TB][VAR].get(), row[headerName][GET_VALUE]()))
                self.setTracesElementTable(REGEX_TRANSLATION_TYPE, idx)

        else:
            print("new translation map file selected:"+fileName)
            swtichTransType = self.translations[headerName][MAP] == NONE
            self.translations[headerName][MAP]=self.vMapFM.readFileToMap(fileName)
            print(self.translations[headerName][MAP])
            if swtichTransType:
                self.transTableComps[idx][PARSER_TB][VAR].set("Num-UnMapped="+str(self.countUnmapped(idx)))
                return
            else:
                #translator
                self.removeTracesTransTable(idx)
                self.transTableComps[idx][PARSER_TB][COMPONENT].configure(state='disabled')
                self.transTableComps[idx][PARSER_TB][VAR].set("Num-UnMapped="+str(self.countUnmapped(idx)))
                self.transTableComps[idx][BUILDER_TB][VAR].set(self.translations[headerName][MAPPING_DEFAULT])
                self.transTableComps[idx][SAMPLE_OUT_LB][VAR].set(self.translateTranslationMap(idx, self.transTableComps[idx][SAMPLE_IN_TB][VAR].get()))
                self.setTracesTransTable(DIRECT_MAP_TRANSLATION_TYPE, idx)
                #table
                self.removeTracesElementTable(idx)
                for rIdx, row in enumerate(self.elements):
                    row[headerName][SAMPLE_OUT_LB][VAR].set(self.translateTranslationMap(idx, row[headerName][GET_VALUE]()))
                self.setTracesElementTable(DIRECT_MAP_TRANSLATION_TYPE, idx)
    def shiftHeader(self, idx, left):
        swapIdx = -1
        if left:
            print("shifting "+str(idx)+" to the left")
            if idx <= 0:
                print("can't move further left")
                return
            else:
                swapIdx = idx-1
        else:
            print("shifting "+str(idx)+" to the right")
            if idx >= len(self.headerOrder)-1:
                print("can't move further right")
                return
            else:
                swapIdx = idx+1
        print("swapping "+str(idx)+"<-->"+str(swapIdx))
        #translationComps
        temp = self.transTableComps[idx]
        self.transTableComps[idx] = self.transTableComps[swapIdx]
        self.transTableComps[swapIdx] = temp
        self.transTableComps[idx][CUSTOM_CATEGORY_MAP_DD][COMPONENT].grid_configure(column=idx+1)
        self.transTableComps[swapIdx][CUSTOM_CATEGORY_MAP_DD][COMPONENT].grid_configure(column=swapIdx+1)
        self.transTableComps[idx][CUSTOM_VALUE_MAP_DD][COMPONENT].grid_configure(column=idx+1)
        self.transTableComps[swapIdx][CUSTOM_VALUE_MAP_DD][COMPONENT].grid_configure(column=swapIdx+1)
        self.transTableComps[idx][ENABLE_HEADER_CB][COMPONENT].grid_configure(column=idx+1)
        self.transTableComps[swapIdx][ENABLE_HEADER_CB][COMPONENT].grid_configure(column=swapIdx+1)
        self.transTableComps[idx][TITLE_LB][FRAME].grid_configure(column=idx+1)
        self.transTableComps[swapIdx][TITLE_LB][FRAME].grid_configure(column=swapIdx+1)
        self.transTableComps[idx][PARSER_TB][COMPONENT].grid_configure(column=idx+1)
        self.transTableComps[swapIdx][PARSER_TB][COMPONENT].grid_configure(column=swapIdx+1)
        self.transTableComps[idx][BUILDER_TB][COMPONENT].grid_configure(column=idx+1)
        self.transTableComps[swapIdx][BUILDER_TB][COMPONENT].grid_configure(column=swapIdx+1)
        self.transTableComps[idx][SAMPLE_IN_TB][COMPONENT].grid_configure(column=idx+1)
        self.transTableComps[swapIdx][SAMPLE_IN_TB][COMPONENT].grid_configure(column=swapIdx+1)
        self.transTableComps[idx][SAMPLE_OUT_LB][COMPONENT].grid_configure(column=idx+1)
        self.transTableComps[swapIdx][SAMPLE_OUT_LB][COMPONENT].grid_configure(column=swapIdx+1)
        #tableComps
        headerName = self.headerOrder[idx]
        swapHeaderName = self.headerOrder[swapIdx]
        #tableHeaders
        self.tableHeaderLabelComps[idx][COMPONENT].grid_configure(column=swapIdx+1)
        self.tableHeaderLabelComps[swapIdx][COMPONENT].grid_configure(column=idx+1)
        temp = self.tableHeaderLabelComps[idx]
        self.tableHeaderLabelComps[idx] = self.tableHeaderLabelComps[swapIdx]
        self.tableHeaderLabelComps[swapIdx] = temp
        #table body
        for row in self.elements:
            row[headerName][FRAME].grid_configure(column=swapIdx+1)
            row[swapHeaderName][FRAME].grid_configure(column=idx+1)
        #headerOrder
        temp = self.headerOrder[idx]
        self.headerOrder[idx] = self.headerOrder[swapIdx]
        self.headerOrder[swapIdx] = temp
        #resetButtonCommands
        self.transTableComps[idx][TITLE_LB][FRAME].grid_configure(column=idx+1)
        self.transTableComps[idx][TITLE_LB][SHIFT_RIGHT_BT].configure(command= lambda *args, i=idx: self.shiftHeader(i, False))
        self.transTableComps[idx][TITLE_LB][SHIFT_LEFT_BT].configure(command= lambda *args, i=idx: self.shiftHeader(i, True))
        self.transTableComps[swapIdx][TITLE_LB][SHIFT_RIGHT_BT].configure(command= lambda *args, i=swapIdx: self.shiftHeader(i, False))
        self.transTableComps[swapIdx][TITLE_LB][SHIFT_LEFT_BT].configure(command= lambda *args, i=swapIdx: self.shiftHeader(i, True))


    def renderTranslator(self, idx, header):
        hComponents = {}
        rowIdx = 0
        hComponents[CUSTOM_CATEGORY_MAP_DD] = {}
        hComponents[CUSTOM_CATEGORY_MAP_DD][VAR] = tkinter.StringVar(value = NONE)
        hComponents[CUSTOM_CATEGORY_MAP_DD][COMPONENT] = ttk.OptionMenu(self.translaterFrame, hComponents[CUSTOM_CATEGORY_MAP_DD][VAR], NONE, *[NONE, *self.cMapFM.getFilesNoExt()], command= lambda *args, i=idx: self.selectCategoryType(i))
        hComponents[CUSTOM_CATEGORY_MAP_DD][COMPONENT].grid(row=rowIdx,column=idx+1,padx=2,pady=1)
        rowIdx += 1
        hComponents[CUSTOM_VALUE_MAP_DD] = {}
        hComponents[CUSTOM_VALUE_MAP_DD][VAR] = tkinter.StringVar(value = NONE)
        hComponents[CUSTOM_VALUE_MAP_DD][COMPONENT] = ttk.OptionMenu(self.translaterFrame, hComponents[CUSTOM_VALUE_MAP_DD][VAR], NONE, *[NONE, *self.vMapFM.getFilesNoExt()], command= lambda *args, i=idx: self.selectTranslationType(i))
        hComponents[CUSTOM_VALUE_MAP_DD][COMPONENT].grid(row=rowIdx,column=idx+1,padx=2,pady=1)
        rowIdx += 1
        hComponents[ENABLE_HEADER_CB] = {}
        hComponents[ENABLE_HEADER_CB][VAR] = tkinter.BooleanVar()
        hComponents[ENABLE_HEADER_CB][COMPONENT] = tkinter.Checkbutton(self.translaterFrame, text="Disabled", variable=hComponents[ENABLE_HEADER_CB][VAR], onvalue=True, offvalue=False, command=lambda *args, i=idx: self.toggleHeaderEnabled(i))
        hComponents[ENABLE_HEADER_CB][COMPONENT].grid(row=rowIdx,column=idx+1,padx=2,pady=1)
        rowIdx += 1
        hComponents[TITLE_LB] = {}
        hComponents[TITLE_LB][FRAME] = tkinter.Frame(self.translaterFrame, background=bgColor1)
        hComponents[TITLE_LB][FRAME].grid(row=rowIdx,column=idx+1,padx=2,pady=1,sticky="ew")
        hComponents[TITLE_LB][FRAME].columnconfigure(0,weight=1)
        hComponents[TITLE_LB][FRAME].columnconfigure(1,weight=1)
        hComponents[TITLE_LB][FRAME].columnconfigure(2,weight=1)
        hComponents[TITLE_LB][VAR] = tkinter.StringVar(value=header)
        hComponents[TITLE_LB][COMPONENT] = tkinter.Label(hComponents[TITLE_LB][FRAME], textvariable=hComponents[TITLE_LB][VAR])
        hComponents[TITLE_LB][COMPONENT].grid(row=0,column=1,padx=0,pady=1)
        hComponents[TITLE_LB][SHIFT_LEFT_BT] = tkinter.Button(hComponents[TITLE_LB][FRAME], text="<", command= lambda *args, i=idx: self.shiftHeader(i, True))
        hComponents[TITLE_LB][SHIFT_LEFT_BT].grid(row=0,column=0,padx=0,pady=0,sticky="w")
        hComponents[TITLE_LB][SHIFT_RIGHT_BT] = tkinter.Button(hComponents[TITLE_LB][FRAME], text=">", command= lambda *args, i=idx: self.shiftHeader(i, False))
        hComponents[TITLE_LB][SHIFT_RIGHT_BT].grid(row=0,column=2,padx=0,pady=0,sticky="e")
        rowIdx += 1
        hComponents[PARSER_TB] = {}
        hComponents[PARSER_TB][VAR] = tkinter.StringVar(value=self.translations[header][PARSER])
        hComponents[PARSER_TB][COMPONENT] = tkinter.Entry(self.translaterFrame, textvariable=hComponents[PARSER_TB][VAR])
        hComponents[PARSER_TB][COMPONENT].grid(row=rowIdx,column=idx+1,padx=2,pady=1)
        hComponents[PARSER_TB][TRACES] = []
        rowIdx += 1
        hComponents[BUILDER_TB] = {}
        hComponents[BUILDER_TB][VAR] = tkinter.StringVar(value=self.translations[header][BUILDER])
        hComponents[BUILDER_TB][COMPONENT] = (tkinter.Entry(self.translaterFrame, textvariable=hComponents[BUILDER_TB][VAR]))
        hComponents[BUILDER_TB][COMPONENT].grid(row=rowIdx,column=idx+1,padx=2,pady=1)
        hComponents[BUILDER_TB][TRACES] = []
        rowIdx += 1
        hComponents[SAMPLE_IN_TB] = {}
        hComponents[SAMPLE_IN_TB][VAR] = tkinter.StringVar(value="HelloWorld")
        hComponents[SAMPLE_IN_TB][COMPONENT] = tkinter.Entry(self.translaterFrame, textvariable=hComponents[SAMPLE_IN_TB][VAR])
        hComponents[SAMPLE_IN_TB][COMPONENT].grid(row=rowIdx,column=idx+1,padx=2,pady=1)
        hComponents[SAMPLE_IN_TB][TRACES] = []
        rowIdx += 1
        hComponents[SAMPLE_OUT_LB] = {}
        hComponents[SAMPLE_OUT_LB][VAR] = tkinter.StringVar(value=self.translateRegxInOut(self.translations[header][PARSER], self.translations[header][BUILDER], hComponents[SAMPLE_IN_TB][VAR].get()))
        hComponents[SAMPLE_OUT_LB][COMPONENT] = (tkinter.Label(self.translaterFrame, textvariable=hComponents[SAMPLE_OUT_LB][VAR]))
        hComponents[SAMPLE_OUT_LB][COMPONENT].grid(row=rowIdx,column=idx+1,padx=2,pady=1)
        return hComponents
    def renderTableHeaderLabel(self, idx, header):
        headerLabelStringVar = tkinter.StringVar(value=header)
        headerLabel = tkinter.Label(self.tableFrame, textvariable=headerLabelStringVar, background=bgColor1 if idx%2 == 0 else bgColor2)
        headerLabel.grid(row=0,column=idx+1,padx=0,pady=0, sticky="nsew")
        self.tableHeaderLabelComps.append({
            VAR: headerLabelStringVar,
            COMPONENT: headerLabel
        })

    def renderTableCell(self, idxr, idxc, header):
        headers = self.elements[idxr]
        cellFrame = tkinter.Frame(self.tableFrame, background=bgColor1 if idxr%2 == 0 else bgColor2)
        cellFrame.grid(row=idxr+1, column=idxc+1, padx=0, pady=0, sticky="nsew")
        headers[header][FRAME] = cellFrame
        destroy, getValue, setValue, trace_add, trace_remove, set_disable, grid_configure = wigitFactory.getWidget(
                headers[header]["type"], cellFrame,
                headers[header]["editable"], self.translateRegxInOut(
                self.translations[header][PARSER],
                self.translations[header][BUILDER],
                headers[header][DEFAULT_VALUE]),
                {"r":0, "c":idxc, "px":defaultSpaceX, "py":defaultSpaceY})
        headers[header][DESTROY] = destroy
        headers[header][GET_VALUE] = getValue
        headers[header][SET_VALUE] = setValue
        headers[header][TRACE_ADD] = trace_add
        headers[header][TRACE_REMOVE] = trace_remove
        headers[header][SET_DISABLE] = set_disable
        headers[header][TRACES] = []
        outputStrVar = tkinter.StringVar(value=self.translateRegxInOut(self.translations[header][PARSER], self.translations[header][BUILDER], getValue()))
        output = tkinter.Label(cellFrame, textvariable=outputStrVar)
        output.grid(row=1, column=idxc, padx=defaultSpaceX, pady=defaultSpaceY)
        headers[header][SAMPLE_OUT_LB] = {
            VAR: outputStrVar,
            COMPONENT: output
        }

    def render(self):
        # Render translation table
        rowIdx = 0
        categoryFileLabel = tkinter.Label(self.translaterFrame, text="OptionalCategoryFile")
        categoryFileLabel.grid(row=rowIdx,column=0,sticky="nsew")
        rowIdx += 1
        translationTypeLabel = tkinter.Label(self.translaterFrame, text="TranslationType")
        translationTypeLabel.grid(row=rowIdx,column=0,sticky="nsew")
        rowIdx += 1
        toggleEnabledLabel = tkinter.Label(self.translaterFrame, text="ToggleEnabled")
        toggleEnabledLabel.grid(row=rowIdx,column=0,sticky="nsew")
        rowIdx += 1
        headerNameLabel = tkinter.Label(self.translaterFrame, text="headerName")
        headerNameLabel.grid(row=rowIdx,column=0,sticky="nsew")
        rowIdx += 1
        parserLabel = tkinter.Label(self.translaterFrame, text="parserRegex")
        parserLabel.grid(row=rowIdx,column=0,sticky="nsew")
        rowIdx += 1
        builderLabel = tkinter.Label(self.translaterFrame, text="builderRegex")
        builderLabel.grid(row=rowIdx,column=0,sticky="nsew")
        rowIdx += 1
        sampleLabel = tkinter.Label(self.translaterFrame, text="input")
        sampleLabel.grid(row=rowIdx,column=0,sticky="nsew")
        rowIdx += 1
        resultLabel = tkinter.Label(self.translaterFrame, text="output")
        resultLabel.grid(row=rowIdx,column=0,sticky="nsew")
        # render translator
        for idx, header in enumerate(self.headerOrder):
            self.transTableComps.append(self.renderTranslator(idx, header))
        # render table
            # headers
        for idx, header in enumerate(self.headerOrder):
            self.renderTableHeaderLabel(idx, header)
            # main table body
        for idx in range(0, len(self.elements)):
            headers = self.elements[idx]
            # render row
            rowLabel = tkinter.Label(self.tableFrame, text="row-"+str(idx))
            rowLabel.grid(row=idx+1,column=0,padx=0,pady=0, sticky="nsew")
            for hIdx, header in enumerate(headers.keys()):
                #render cell
                self.renderTableCell(idx,hIdx,header)
            # render omitted rows count
            self.numClippedRowsLabel[VAR] = tkinter.StringVar(value="..."+str(self.numHidden))
            self.numClippedRowsLabel[COMPONENT] = tkinter.Label(self.tableFrame, textvariable=self.numClippedRowsLabel[VAR])
            self.numClippedRowsLabel[COMPONENT].grid(row=len(self.elements)+1, column=0, columnspan=len(self.headerOrder)+1)

        # Set Tracers
        for cIdx, header in enumerate(self.transTableComps):
            self.setTracesTransTable(REGEX_TRANSLATION_TYPE, cIdx)
            self.setTracesElementTable(REGEX_TRANSLATION_TYPE, cIdx)
        #render buttons
        resolveButton = tkinter.Button(self.buttonsFrame, text="RESOLVE", command=lambda *args:self.resolveThis(self.categoryMaps))
        resolveButton.grid(row=0,column=0,padx=30,pady=10)

    def getValues(self):
        values = []
        for idx, headers in enumerate(self.elements):
            values.append({})
            for header in headers.keys():
                values[idx][header] = headers[header][SAMPLE_OUT_LB][VAR].get()
        return values

    def resolveThis(self, catMap):
        for header in self.headerOrder:
            if not catMap[header] == None:
                file = self.categoryMaps[header]
                catMap[header]=None
                categoryMap = file[FILE_MANAGER].loadCategoryFile(file[FILE_NAME], ext=FILE_EXT)
                categoryElementList = []
                for arr in categoryMap.values():
                    categoryElementList+=arr
                unTrackedVals=[]
                for element in self.elements:
                    val = element[header][SAMPLE_OUT_LB][VAR].get()
                    if not categoryElementList.__contains__(val):
                        unTrackedVals.append(val)
                if len(unTrackedVals)>0:
                    ModalWrapper(EditCategoryFileModule, "CategoryEditing", elements=unTrackedVals, otherOptions=file, handleResolveValue=lambda *args, value, cM=catMap:self.resolveThis(cM))
                    return
        self.resolve()

    def removeTracesTransTable(self, columnIdx):
        for trace in self.transTableComps[columnIdx][PARSER_TB][TRACES]:
            self.transTableComps[columnIdx][PARSER_TB][VAR].trace_remove("write", trace)
        self.transTableComps[columnIdx][PARSER_TB][TRACES] = []
        for trace in self.transTableComps[columnIdx][BUILDER_TB][TRACES]:
            self.transTableComps[columnIdx][BUILDER_TB][VAR].trace_remove("write", trace)
        self.transTableComps[columnIdx][BUILDER_TB][TRACES] = []
        for trace in self.transTableComps[columnIdx][SAMPLE_IN_TB][TRACES]:
            self.transTableComps[columnIdx][SAMPLE_IN_TB][VAR].trace_remove("write", trace)
        self.transTableComps[columnIdx][SAMPLE_IN_TB][TRACES] = []
    def setTracesTransTable(self, translationType, columnIdx):
        if translationType == REGEX_TRANSLATION_TYPE:
            headerName = self.headerOrder[columnIdx]
            self.transTableComps[columnIdx][PARSER_TB][TRACES].append(self.transTableComps[columnIdx][PARSER_TB][VAR].trace_add("write", lambda *args, h=headerName: self.updateTransitions(h, parserStr=True)))
            self.transTableComps[columnIdx][BUILDER_TB][TRACES].append(self.transTableComps[columnIdx][BUILDER_TB][VAR].trace_add("write", lambda *args, h=headerName: self.updateTransitions(h, builderStr=True)))
            self.transTableComps[columnIdx][SAMPLE_IN_TB][TRACES].append(self.transTableComps[columnIdx][SAMPLE_IN_TB][VAR].trace_add("write", lambda *args, h=headerName: self.updateTransitionSampleInput(h)))
        elif translationType == DIRECT_MAP_TRANSLATION_TYPE:
            self.transTableComps[columnIdx][BUILDER_TB][TRACES].append(self.transTableComps[columnIdx][BUILDER_TB][VAR].trace_add("write", lambda *args, i=columnIdx: self.transMapUpdateDefault(i)))
            self.transTableComps[columnIdx][SAMPLE_IN_TB][TRACES].append(self.transTableComps[columnIdx][SAMPLE_IN_TB][VAR].trace_add("write", lambda *args,i=columnIdx: self.transTableComps[columnIdx][SAMPLE_OUT_LB][VAR].set(self.translateTranslationMap(i, self.transTableComps[i][SAMPLE_IN_TB][VAR].get()))))
    def removeTracesElementTable(self, columnIdx):
        headerName = self.headerOrder[columnIdx]
        for rIdx, row in enumerate(self.elements):
            for trace in row[headerName][TRACES]:
                row[headerName][TRACE_REMOVE]("write", trace)
            row[headerName][TRACES] = []
    def setTracesElementTable(self, translationType, columnIdx):
        headerName = self.headerOrder[columnIdx]
        if translationType == REGEX_TRANSLATION_TYPE:
            for rIdx, row in enumerate(self.elements):
                row[headerName][TRACES].append(row[headerName][TRACE_ADD]("write", lambda *args, h=headerName, idx = rIdx: self.updateTableOutput(idx, h)))
        elif translationType == DIRECT_MAP_TRANSLATION_TYPE:
            for rIdx, row in enumerate(self.elements):
                row[headerName][TRACES].append(row[headerName][TRACE_ADD]("write", lambda *args, ci=columnIdx, ri=rIdx, h=headerName: self.elements[ri][h][SAMPLE_OUT_LB][VAR].set(self.translateTranslationMap(ci, self.elements[ri][h][GET_VALUE]()))))


    def translateTranslationMap(self, idx, inText):
        print("idx="+str(idx)+"\theader="+self.headerOrder[idx])
        translation = self.translations[self.headerOrder[idx]]
        if translation[MAP].__contains__(inText):
            return translation[MAP][inText]
        else:
            return self.transTableComps[idx][BUILDER_TB][VAR].get()
    def translateRegxInOut(self, parser, builder, inText):
        values = []
        self.parseInText(parser, inText, values)
        return self.buildOutText(builder, values)

    # %s for values in the parser
    def parseInText (self, parserStr, inText, values):
        checkVals = parserStr.split("%s")
        if len(checkVals) == 1:
            values.append(inText)
            return True
        inTextIdx = 0
        pcv = checkVals[0]
        if inText.startswith(pcv):
            inTextIdx = len(pcv)
        else:
            return False
        for checkVal in checkVals[1:]:
            inTextIdxNext = len(inText) if checkVal=="" else inText.find(checkVal, inTextIdx)
            if inTextIdxNext == -1:
                values.append(inText[inTextIdx:])
                return False
            else:
                values.append(inText[inTextIdx:inTextIdxNext])
                inTextIdx = inTextIdxNext+len(checkVal)
        return True


    def buildOutText(self, builderStr, values):
        if builderStr == "":
            return "".join(values)
        bs=builderStr
        subStrs = []
        for idx in range(0,len(values)):
            subStrs.append("%s"+str(idx))
        for idx in range(len(values)-1, -1, -1):
            bs=bs.replace(subStrs[idx], values[idx])
        return bs
        # strBits = builderStr.split("%s")
        # # No %s found.
        # if len(strBits)==1:
        #     return builderStr
        # sb=""
        # for idx, strBit in enumerate(strBits):
        #     if idx < len(values):
        #         sb+=strBit+values[idx]
        #     else:
        #         sb+=strBit
        # return sb

    def destroy(self):
        for element in self.elements:
            for item in element.items():
                item[DESTROY]()
        super().destroy()

    def updateData(self, elements):
        if len(elements) < 1:
            return
        oldHlen = len(self.headerOrder)
        newHlen = len(elements[0])
        newHeaderOrder = list(elements[0].keys())


        #reset translations
        if newHlen > oldHlen: #Add to
            oldtranslations = self.translations
            self.translations = {}
            for idx, headerName in enumerate(self.headerOrder):
                self.translations[newHeaderOrder[idx]]=oldtranslations[headerName]
                self.transTableComps[idx][TITLE_LB][VAR].set(newHeaderOrder[idx])
            for idx in range(len(self.headerOrder), len(newHeaderOrder)):
                self.translations[newHeaderOrder[idx]]={
                    PARSER:"",
                    BUILDER:""}
                self.transTableComps.append(self.renderTranslator(idx, newHeaderOrder[idx]))
        elif newHlen == oldHlen: #Stays the same size
            oldtranslations = self.translations
            self.translations = {}
            for idx, headerName in enumerate(newHeaderOrder):
                self.translations[headerName]=oldtranslations[self.headerOrder[idx]]
                self.transTableComps[idx][TITLE_LB][VAR].set(headerName)
        else: # newHlen < oldHlen #remove from
            oldtranslations = self.translations
            self.translations = {}
            for idx, headerName in enumerate(newHeaderOrder):
                self.translations[headerName]=oldtranslations[self.headerOrder[idx]]
                self.transTableComps[idx][TITLE_LB][VAR].set(headerName)
            rmIdx = len(newHeaderOrder)
            for idx in range(len(newHeaderOrder), len(self.headerOrder)):
                self.translations.pop(self.headerOrder[idx])
                self.removeTracesTransTable(idx)
                self.transTableComps[idx][ENABLE_HEADER_CB][COMPONENT].destroy()
                self.transTableComps[idx][CUSTOM_CATEGORY_MAP_DD][COMPONENT].destroy()
                self.transTableComps[idx][CUSTOM_VALUE_MAP_DD][COMPONENT].destroy()
                self.transTableComps[idx][ENABLE_HEADER_CB][COMPONENT].destroy()
                self.transTableComps[idx][TITLE_LB][FRAME].destroy()
                self.transTableComps[idx][PARSER_TB][COMPONENT].destroy()
                self.transTableComps[idx][BUILDER_TB][COMPONENT].destroy()
                self.transTableComps[idx][SAMPLE_IN_TB][COMPONENT].destroy()
                self.transTableComps[idx][SAMPLE_OUT_LB][COMPONENT].destroy()
                self.transTableComps.pop(rmIdx)

        #update table Headers
        if newHlen > oldHlen:
            for idx in range(0,oldHlen):
                self.tableHeaderLabelComps[idx][VAR].set(newHeaderOrder[idx])
            for idx in range(oldHlen, newHlen):
                self.renderTableHeaderLabel(idx, newHeaderOrder[idx])
        elif newHlen < oldHlen:
            for idx in range(0,newHlen):
                self.tableHeaderLabelComps[idx][VAR].set(newHeaderOrder[idx])
            for idx in range(newHlen, oldHlen):
                self.tableHeaderLabelComps[idx][COMPONENT].destroy()
        else: #newHlen == oldHlen:
            for idx in range(0,newHlen):
                self.tableHeaderLabelComps[idx][VAR].set(newHeaderOrder[idx])
        #destroy table
        for cIdx in range(0, len(self.headerOrder)):
            self.removeTracesElementTable(cIdx)
        for headers in self.elements:
            for value in headers.values():
                value[DESTROY]()
                value[SAMPLE_OUT_LB][COMPONENT].destroy()
        #generate new table
        self.numHidden = len(elements) - len(self.elements)
        self.elements = elements[0:len(self.elements)]
        for idxr, headers in enumerate(self.elements):
            for idxc, headerName in enumerate(headers.keys()):
                self.renderTableCell(idxr,idxc,headerName)
        self.headerOrder = newHeaderOrder
        self.updateHeaders(self.headerOrder)
        #update hidden rows count
        self.numClippedRowsLabel[VAR] = tkinter.StringVar(value="..."+str(self.numHidden))
        #create new traces
        if newHlen > oldHlen:
            for cIdx in range(oldHlen, newHlen):
                self.setTracesTransTable(REGEX_TRANSLATION_TYPE, cIdx)
                self.setTracesElementTable(REGEX_TRANSLATION_TYPE, cIdx)