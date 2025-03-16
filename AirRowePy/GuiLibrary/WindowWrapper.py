import tkinter

class RootWindow():
    # Contains
    #   -Window
    #   -Frame (container in window that holds components)
    def __init__(self, title):
        self.window = tkinter.Tk()
        self.window.title(title)
        self.mainFrame = tkinter.Frame(self.window)
    def show(self):
        self.mainFrame.grid()
        self.window.mainloop()
    def hide(self):
        self.mainFrame.pack_forget()
    def destroy(self):
        self.window.destroy()
    def getRoot(self):
        return self.mainFrame
