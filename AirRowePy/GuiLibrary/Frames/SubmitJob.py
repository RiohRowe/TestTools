import tkinter

class GridFrameHandler():
    grid={"row":0, "column":0, "padx":0, "pady":0}
    def __init__(self, parent):
        self.parentFrame = parent
        self.frame = tkinter.Frame(parent)

    def show(self):
        self.frame.grid(row=self.grid.get("row"), column=self.grid.get("column"), padx=self.grid.get("padx"), pady=self.grid.get("pady"))
    def hide(self):
        self.frame.grid_remove()
    def destroy(self):
        self.frame.destroy()
