import tkinter
from math import floor

from AirRowePy.GuiLibrary.Frames.FrameWrapper import GridFrame

class TextEntryFrame(GridFrame):
    # elements structure:
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
    #]
    def __init__(self, parent, handleData, headerOrder=["h1","h2"], grid={"r":0, "c":0, "px":0, "py":0}):
        super().__init__(parent, grid)
        self.handleData = handleData
        self.headerOrder = headerOrder
        self.tableData = []
        self.headerEntries = []
        self.render()


    def render(self):
        # Render translation table
        self.textBoxLabel = tkinter.Label(self.frame, text="Enter Bulk Data")
        self.textBoxLabel.grid(row=0,column=0,sticky="nsew",columnspan=len(self.headerOrder))
        for idx,header in enumerate(self.headerOrder):
            headerEntry = (tkinter.Entry(self.frame))
            headerEntry.insert(0, header)
            headerEntry.grid(row=1,column=idx,sticky="nsew")
            self.headerEntries.append(headerEntry)
        self.textBox = tkinter.Text(self.frame)
        self.textBox.grid(row=2, column=0, columnspan=len(self.headerOrder))

        self.updateFormButton = tkinter.Button(self.frame, text="update-headers", command=self.updateHeaders)
        self.updateFormButton.grid(row=3,column=0)

        self.getDataButton = tkinter.Button(self.frame, text="transform-data", command=self.getData)
        self.getDataButton.grid(row=3,column=1)

    def updateHeaders(self):
        dataStr = self.textBox.get(1.0,'end-1c')
        print("dataStr")
        print(dataStr)
        if len(dataStr) == 0:
            return
        rows = dataStr.split('\n')
        newNumHeaders = rows[0].count('\t')+1
        oldNumHeaders = len(self.headerOrder)
        if oldNumHeaders == newNumHeaders:
            return
        if oldNumHeaders < newNumHeaders:
            for idx in range(oldNumHeaders, newNumHeaders):
                self.headerOrder.append("h"+str(idx+1))
                headerEntry = (tkinter.Entry(self.frame))
                headerEntry.insert(0, self.headerOrder[idx])
                headerEntry.grid(row=1,column=idx,sticky='nsew')
                self.headerEntries.append(headerEntry)
        else:
            for idx in range(newNumHeaders,oldNumHeaders):
                self.headerOrder.pop()
                self.headerEntries[newNumHeaders].destroy()
                self.headerEntries.pop(newNumHeaders)
        self.textBoxLabel.grid_configure(columnspan=newNumHeaders)
        self.textBox.grid_configure(columnspan=newNumHeaders)
        if newNumHeaders < 2:
            self.updateFormButton.grid_configure(columnspan=1)
            self.getDataButton.grid_configure(columnspan=1)
        else:
            self.updateFormButton.grid_configure(columnspan=floor(newNumHeaders/2))
            self.getDataButton.grid_configure(column=floor(newNumHeaders/2)+1,columnspan=floor(newNumHeaders/2))




    def getData(self):
        self.elements = []
        dataStr = self.textBox.get(1.0,'end-1c')
        for idx, row in enumerate(dataStr.split('\n')):
            self.elements.append({})
            for hidx, column in enumerate(row.split('\t')):
                self.elements[idx][self.headerEntries[hidx].get()] = {
                    "type":"t",
                    "editable":True,
                    "defaultValue":column}
        self.handleData(self.elements)


