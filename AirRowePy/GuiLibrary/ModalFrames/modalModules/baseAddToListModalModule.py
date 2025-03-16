import tkinter.ttk

from AirRowePy.GuiLibrary.FileManager import FileManager
from AirRowePy.GuiLibrary.Frames.FrameWrapper import GridFrame
from AirRowePy.GuiLibrary.ModalFrames.WigitFactory import WigitFactory
from AirRowePy.GuiLibrary.ModalFrames.modalModules.AddToListModalComponents.RowTranslatorTableFrame import \
    RowTranslatorTableFrame, DESTROY
from AirRowePy.GuiLibrary.ModalFrames.modalModules.AddToListModalComponents.TextEntryFrame import TextEntryFrame


# entry structure:
    #[
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
    def __init__(self, parent,resolve,
                 elements=[{"h1":{"type": "t", "editable": False, "defaultValue": "defaultValue"}}],
                 grid={"r": 0, "c": 0, "px": 0, "py": 0}) -> None:
        super().__init__(parent, grid=grid)
        for idx, hs in enumerate(elements):
            for h in hs.keys():
                keys = hs[h].keys()
                if not keys.__contains__("type"):
                    hs[h]["type"] = defaultWigitType
                if not keys.__contains__("editable"):
                    hs[h]["editable"] = defaultEditable
                if not keys.__contains__("defaultValue"):
                    hs[h]["defaultValue"] = None
        self.headerOrder = list(elements[0].keys())
        self.elements = elements
        self.resolve = resolve
        self.fm = FileManager("./files/translationMaps")
        self.render()

    def render(self):
        self.rowTranslatorTableFrame = RowTranslatorTableFrame(self.frame, self.elements[0:5], len(self.elements), self.resolve, grid={"r":0, "c":0, "px":0, "py":0})
        self.rowTranslatorTableFrame.frame.grid_configure(rowspan=2)
        #buttons
        options = self.fm.getFilesNoExt()
        firstOption = options[0] if len(options)>0 else ""
        self.fileMapSelectorDropDownVar = tkinter.StringVar(value=firstOption)
        self.fileMapSelectorDropDown = tkinter.ttk.OptionMenu(self.frame, self.fileMapSelectorDropDownVar, firstOption,options)
        self.fileMapSelectorDropDown.grid(row=0,column=3,padx=0,pady=0,sticky="nsew")
        self.addMappingFileButton = tkinter.Button(self.frame, text="newMapFile", command=lambda *args, h=self.fileMapSelectorDropDownVar.get(): self.rowTranslatorTableFrame.addMap())
        self.addMappingFileButton.grid(row=0,column=1,padx=0,pady=0,sticky="nsew")
        self.editMappingFileButton = tkinter.Button(self.frame, text="editMapFile", command=lambda *args, f=self.fileMapSelectorDropDownVar.get(): self.rowTranslatorTableFrame.editMap(f))
        self.editMappingFileButton.grid(row=0,column=2,padx=0,pady=0,sticky="nsew")
        self.entryFrame = TextEntryFrame(self.frame, self.updateTranslatorTable, headerOrder=self.headerOrder, grid={"r":1, "c":1, "px":0, "py":0})
        self.entryFrame.frame.grid_configure(columnspan=3)

    def getValues(self):
        return self.rowTranslatorTableFrame.getValues()
    def updateTranslatorTable(self, elements):
        self.rowTranslatorTableFrame.updateData(elements)
    # def getComponent(self, parent):
    #     return tkinter.Frame(parent)
    # # render and reveal updates to value object
    # def show(self):
    #     self.frame.grid(row=self.grid["r"], column=self.grid["c"], padx=self.grid["px"], pady=self.grid["py"])
    # # un-render  components
    # def hide(self):
    #     self.frame.grid_remove()
    # # remove component
    def destroy(self):
        for headers in self.elements:
            for header in headers.values():
                header[DESTROY]()
        super().destroy()
    # # change relative position reference. Used by show method.
    # def update(self, newPos):
    #     for key in self.grid:
    #         if key in newPos:
    #             self.grid[key] = newPos[key]
    #     if self.frame.grid_info():
    #         self.show()
