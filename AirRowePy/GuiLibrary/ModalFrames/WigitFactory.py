#Abstracts Wigit creation and deletion to text based selection, and simple add/remove functions
import tkinter


class WigitFactory():
    def __init__(self):
        self.defaultText = "default"
        self.defaultNum = 0
        self.map = {
            "t": self.editTextWigit
        }
    def getWidget(self, ref, parent, editable, value, grid={"r":0, "c":0, "px":0, "py":0}):
        if not self.map.__contains__(ref):
            ref = "t"
        return self.map[ref](parent,editable,value,grid)
    # wigit functions returns tupple of the function to
    #   -delete the component,
    #   -get the component value
    #   -set the component value
    #   -add a trace for the component value
    #   -remove a trace for the component value
    #   -enable/disable component
    #   -configure component grid
    def editTextWigit(self, parent, editable, value, grid): #-> (destroyFunc, getValueFunc, setValueFunc, addTraceFunc, removeTraceFunc, setDisabledFunc, configureGrid)
        fieldEntryVar = tkinter.StringVar(value=value if isinstance(value, str) else self.defaultText)
        fieldEntry = tkinter.Entry(parent,
                                   state="normal" if editable else "disabled",
                                   textvariable=fieldEntryVar,
                                   width=20)
        fieldEntry.grid(row=grid["r"],column=grid["c"],padx=grid["px"],pady=grid["py"])
        return(fieldEntry.destroy, fieldEntryVar.get, fieldEntryVar.set, fieldEntryVar.trace_add, fieldEntryVar.trace_remove, lambda *args, disabled: fieldEntry.configure(state='disabled' if disabled else 'normal'), fieldEntry.grid_configure)
    # def editNumWidget(self, parent, editable, value, grid):
    # def editDateWidgetYMD(self, parent, editable, value, grid):
