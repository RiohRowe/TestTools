import tkinter

class ModalWrapper():
    # Contains
    #   -Window
    #   -Frame (container in window that holds components)
    def __init__(self, modalModule, title,
                 elements,
                 handleResolveValue=lambda *args, value: print("returnValue=\n"+str(value)+"\n"),
                 grid={"r": 0, "c": 0, "px": 0, "py": 0}):
        self.window = tkinter.Toplevel()
        self.window.title(title)
        print("ELEMENTS1=\n"+str(elements)+"\n\n")
        self.modalModule = modalModule(self.window,self.resolve,elements,grid)
        self.handleResolve=handleResolveValue
        print("MODAL_MODULE="+str(self.modalModule))
        self.show()
    def resolve(self):
        #   get values
        vals = self.modalModule.getValues()
        #   close window
        self.destroy()
        #   return values
        self.handleResolve(value=vals)
    def show(self):
        self.modalModule.show()
        self.window.mainloop()
    def hide(self):
        self.modalModule.getRoot.pack_forget()
    def destroy(self):
        self.modalModule.destroy()
        self.window.destroy()
    def getRoot(self):
        return self.modalModule.getRoot()
