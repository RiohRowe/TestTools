import tkinter

from .FrameWrapper import GridFrame

#
class EditableStringListComponent(GridFrame):
    listName = "defaultListName"
    # List of elements
    listContent = [{"defaultHeader1":"one", "defaultHeader2":"two"}]
    headers=[]
    listSelections = []
    def update(self, position, listName, listContent):
        if not listName == None:
            self.listName = listName
        if not listContent == None and type(listContent) == [].__class__ :
            self.listContent = listContent
            self.headers = [];
            for element in self.listContent:
                for key in element.keys():
                    if not key in self.headers:
                        self.headers.append(key)

        if position:
            super().update(position)
    def refresh(self):
        for child in self.children:
            child.destroy()
        for selection in self.listSelections:
            selection.destroy()

        self.frame.configure(text=self.listName)

        for content in self.listContent:
            selectedVar = tkinter.BooleanVar(value=False)
            self.listSelections.append(selectedVar)


        label = tkinter.Label(self.frame, text=self.listName)
        label.grid(row=0,column=0,padx=10,pady=10)
        self.children.add(label)
        for


    def __init__(self, parent, listName, listContent):
        self.grid["px"]=10
        self.grid["py"]=10
        print(self.grid)
        super().__init__(parent)
