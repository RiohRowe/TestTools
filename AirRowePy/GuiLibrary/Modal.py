import tkinter

from AirRowePy.GuiLibrary.WindowWrapper import RootWindow


class Modal():

    def __init__(self, title):
        self.modal =  RootWindow(title)
    def getRootFrame(self):
        return self.modal.getRoot()
