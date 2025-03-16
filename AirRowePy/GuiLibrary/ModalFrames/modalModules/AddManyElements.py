from AirRowePy.GuiLibrary.Frames.FrameWrapper import GridFrame


class baseModalModule(GridFrame):
    def getValues(self):
        return("default value")
    def getComponent(self, parent):
        return tkinter.Frame(parent)
    def __init__(self, parent, headers=[{"header":"h1", "type":"t","editable":false, "defaultValue":"defaultValue"}], grid={"r":0, "c":0, "px":0, "py":0}) -> None:
        self.parent = parent
        self.frame = self.getComponent(parent)
        self.grid=grid
        self.show()

    # render and reveal updates to value object
    def show(self):
        self.frame.grid(row=self.grid["r"], column=self.grid["c"], padx=self.grid["px"], pady=self.grid["py"])
    # un-render  components
    def hide(self):
        self.frame.grid_remove()
    # remove component
    def destroy(self):
        for child in self.children:
            child.destroy()
        self.frame.destroy()
    # change relative position reference. Used by show method.
    def update(self, newPos):
        for key in self.grid:
            if key in newPos:
                self.grid[key] = newPos[key]
        if self.frame.grid_info():
            self.show()
