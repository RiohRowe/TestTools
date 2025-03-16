import tkinter

from Tools.scripts.texi2html import increment

from .FrameWrapper import GridFrame

#
class MoreListComponent(GridFrame):
    def extendCompontents(self):
        numAddedElements = self.incrament if self.elementsLeft > self.incrament else self.elementsLeft
        self.elementsLeft -= numAddedElements
        self.extendFunc(numAddedElements, self.moreUp)
        if self.elementsLeft == 0:
            self.destroy()
        else:
            self.seeMoreButton.configure(text=self.genButtonText())

    def genButtonText(self):
        howManyMore=self.elementsLeft if self.incrament>self.elementsLeft else self.incrament
        up = "^" if self.moreUp else "v"
        return "view "+str(howManyMore)+"/"+str(self.elementsLeft)+" more "+up
    def refresh(self):
        # delete all components
        for child in self.children:
            child.destroy()
        self.children = []
        # create new content
        self.seeMoreButton = tkinter.Button(self.frame, text=self.genButtonText(), command=self.extendCompontents)
        self.seeMoreButton.grid(row=0,column=0,padx=10,pady=5)
        self.children.append(self.seeMoreButton)

    def __init__(self, parent, amount, moreUp=True, incrament=10, grid=None, extendFunc=None):
        if amount==0:
            return
        if not grid:
            if moreUp:
                grid={"r":0,"c":0,"px":0,"py":0}
            else:
                grid={"r":2,"c":0,"px":0,"py":0}

        self.elementsLeft = amount
        self.moreUp = moreUp
        self.incrament = incrament
        if not extendFunc == None:
            self.extendFunc = extendFunc
        else:
            self.extendFunc = lambda amount, moreUp: print("adding "+str(amount)+ "elements")
        super().__init__(parent, grid)
        self.refresh()
