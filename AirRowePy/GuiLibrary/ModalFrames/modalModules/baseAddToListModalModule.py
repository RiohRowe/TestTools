import tkinter.ttk

from AirRowePy.GuiLibrary.FileManager import FileManager
from AirRowePy.GuiLibrary.Frames.FrameWrapper import GridFrame
from AirRowePy.GuiLibrary.ModalFrames.modalModules.AddToListModalComponents.RowTranslatorTableFrame import \
    RowTranslatorTableFrame, DESTROY
from AirRowePy.GuiLibrary.ModalFrames.modalModules.AddToListModalComponents.TextEntryFrame import TextEntryFrame


# entry structure:
    #
    #   {
    #       Header1: {
    #           "type": var type (EX: "t"-text, "n"-number, "dymd"-dateYearMonthDay)
    #           "editable": allow editing of value? (EX: True, False)
    #           "defaultValue": starting value (EX: "HelloWorld", 1, 2025/1/24)
    #           "getVal": function for getting the current value
    #           "destroy": function for deleting the wigit
    #       },
    #       Header2: {...},
    #       Header3: {...},
    #       Header4: {...}
    #   }

defaultWigitType="t"
defaultEditable=True

class BaseAddElementsModalModule(GridFrame):
    def __init__(self, parent,resolve, elements={}, otherOptions={},
                 grid={"r": 0, "c": 0, "px": 0, "py": 0}) -> None:
        super().__init__(parent, grid=grid)
        self.headerOrder = list(elements[0].keys())
        self.elements = elements
        self.resolve = resolve
        self.fm = FileManager(FileManager.TRANSLATION_MAP_FILES_PATH)
        self.render()
    
    def updateHeaders(self,newHeaderOrder):
        self.headerOrder=newHeaderOrder
        if not newHeaderOrder.__contains__(self.headerSelectorDropDownVar.get()):
            self.headerSelectorDropDownVar.set(newHeaderOrder[0])
        gridInfo = self.headerSelectorDropDown.grid_info()
        self.headerSelectorDropDown.destroy()
        self.headerSelectorDropDown = tkinter.ttk.OptionMenu(self.frame, self.headerSelectorDropDownVar, self.headerSelectorDropDownVar.get(),*self.headerOrder)
        self.headerSelectorDropDown.grid(gridInfo)
        
    def addMap(self):
        print("HEADER = "+self.headerSelectorDropDownVar.get())
        self.rowTranslatorTableFrame.addMap(self.headerSelectorDropDownVar.get())
    def editMap(self):
        self.rowTranslatorTableFrame.editMap(self.fileMapSelectorDropDownVar.get())
    def render(self):
        self.rowTranslatorTableFrame = RowTranslatorTableFrame(self.frame, self.elements[0:5], len(self.elements), self.resolve, self.updateHeaders, grid={"r":0, "c":0, "px":0, "py":0})
        self.rowTranslatorTableFrame.frame.grid_configure(rowspan=2)
        #buttons
        options = self.fm.getFilesNoExt()
        firstOption = options[0] if len(options)>0 else ""
        self.fileMapSelectorDropDownVar = tkinter.StringVar(value=firstOption)
        self.fileMapSelectorDropDown = tkinter.ttk.OptionMenu(self.frame, self.fileMapSelectorDropDownVar, firstOption,*options)
        self.fileMapSelectorDropDown.grid(row=0,column=4,padx=0,pady=0,sticky="nsew")
        self.headerSelectorDropDownVar = tkinter.StringVar(value=self.headerOrder[0])
        self.headerSelectorDropDown = tkinter.ttk.OptionMenu(self.frame, self.headerSelectorDropDownVar, self.headerOrder[0],*self.headerOrder)
        self.headerSelectorDropDown.grid(row=0,column=2,padx=0,pady=0,sticky="nsew")
        self.addMappingFileButton = tkinter.Button(self.frame, text="newMapFile", command=self.addMap)
        self.addMappingFileButton.grid(row=0,column=1,padx=0,pady=0,sticky="nsew")
        self.editMappingFileButton = tkinter.Button(self.frame, text="editMapFile", command=self.editMap)
        self.editMappingFileButton.grid(row=0,column=3,padx=0,pady=0,sticky="nsew")
        self.entryFrame = TextEntryFrame(self.frame, self.updateTranslatorTable, headerOrder=self.headerOrder, grid={"r":1, "c":1, "px":0, "py":0})
        self.entryFrame.frame.grid_configure(columnspan=3)

    def getValues(self):
        return self.rowTranslatorTableFrame.getValues()
    def updateTranslatorTable(self, elements):
        self.rowTranslatorTableFrame.updateData(elements)
    def destroy(self):
        for headers in self.elements:
            for header in headers.values():
                header[DESTROY]()
        super().destroy()
