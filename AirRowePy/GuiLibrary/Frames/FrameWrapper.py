import tkinter
from tkinter import ttk


class GridFrame:
    # Returns the Component being wrappered
    def getComponent(self, parent):
        return tkinter.Frame(parent)
    def __init__(self, parent, grid={"r":0, "c":0, "px":0, "py":0}) -> None:
        self.parent = parent
        self.frame = self.getComponent(parent)
        self.grid=grid
        self.frame.grid(row=self.grid["r"], column=self.grid["c"], padx=self.grid["px"], pady=self.grid["py"])
    # render and reveal updates to value object
    def show(self):
        self.frame.grid(row=self.grid["r"], column=self.grid["c"], padx=self.grid["px"], pady=self.grid["py"])
    # un-render  components
    def hide(self):
        self.frame.grid_remove()
    # remove component
    def destroy(self):
        # Destroying a frame calls destroy() on all nested components
        self.frame.destroy()
    # change relative position reference. Used by show method.
    def update(self, newPos):
        for key in self.grid:
            if key in newPos:
                self.grid[key] = newPos[key]
        if self.frame.grid_info():
            self.show()

class PackFrame:
    pack={"e":0, "f":"none", "s":"top"}
    def getComponent(self, parent):
        return tkinter.Frame(parent)
    def __init__(self, parent) -> None:
        self.parent = parent
        self.frame = self.getComponent(parent)
        self.frame.pack(expand=self.pack["e"], fill=self.pack["f"], side=self.pack["s"])
    def show(self):
        self.frame.pack(expand=self.pack["e"], fill=self.pack["f"], side=self.pack["s"])
    def hide(self):
        self.frame.pack_forget()
    def destroy(self):
        # Destroying a frame calls destroy() on all nested components
        self.frame.destroy()
    def update(self, newPos):
        for key in self.pack:
            if key in newPos:
               self.pack[key] = newPos[key]
        if not self.frame.grid_info():
            self.show()

class ScrollGridFrame(PackFrame):
    def getComponent(self, parent):
        self.outerFrame = tkinter.Frame(parent)
        self.outerFrame.pack(side='right', fill='both', expand=1)
        return self.outerFrame
    def getInnerFrame(self):
        return self.frame
    def getContentSize(self):
        # print("GettingContentSize")
        return (0,0,self.frame.winfo_width(),self.frame.winfo_height())
    def destroy(self):
        super().destroy()
        self.canvasScrollBar.destroy()
        self.tableDisplayCanvas.destroy()


    def __init__(self, parent, height=500, width=700):
        super().__init__(parent)
        parent.configure(highlightbackground="black", highlightthickness=2)
        self.tableDisplayCanvas = tkinter.Canvas(self.outerFrame, height=height, width=width)
        self.tableDisplayCanvas.pack(side='left', fill='both', expand=1)
        self.canvasScrollBar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tableDisplayCanvas.yview)
        self.canvasScrollBar.pack(side="right", fill='y')
        self.tableDisplayCanvas.configure(yscrollcommand=self.canvasScrollBar.set)
        # self.tableDisplayCanvas.bind('<Configure>',
        #                         # lambda e: self.tableDisplayCanvas.configure(scrollregion=(0,0,1000,3000)))
        #                         lambda e: self.tableDisplayCanvas.configure(scrollregion=self.getContentSize()))
        self.frame = tkinter.Frame(self.tableDisplayCanvas)
        self.frame.bind('<Configure>',
                                     # lambda e: self.tableDisplayCanvas.configure(scrollregion=(0,0,1000,3000)))
                                     lambda e: self.tableDisplayCanvas.configure(scrollregion=self.getContentSize()))
        self.tableDisplayCanvas.create_window((0, 0), window=self.frame, anchor='nw')