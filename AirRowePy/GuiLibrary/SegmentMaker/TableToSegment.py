import csv
import os
import tkinter
from tkinter import ttk

root_path = os.path.dirname(__file__)
# fileName = "EHSegmentTable.txt"
# fileName = "EHNSegmentTable.txt"
fileName = "ER2SegmentTable.txt"
# fileName = "ER3SegmentTable.txt"
# fileName = "ER4SegmentTable.txt"
# fileName = "ER4JSegmentTable.txt"
# fileName = "ER5SegmentTable.txt"
input_file = []
delimiter = "\t"

#Main Window
window = tkinter.Tk()
window.title("SegmentParser")

segData = []

segmentComponentList = []
optionComponents = []
segmentInputVar = tkinter.StringVar(value="placeholder")


FIELD_NAME = "FIELD_NAME"
FIELD_INDEX = "FIELD_INDEX"
FIELD_VALUE = "FIELD_VALUE"
FIELD_SIZE = "FIELD_SIZE"
INPUT_COMPONENT_VAR = "INPUT_COMPONENT_VAR"
INPUT_COMPONENT = "INPUT_COMPONENT"


def tableToSegmentSync():
    global segmentInputVar
    segment = segmentFromData()
    print(segment)
    segmentInputVar.set(segment)


def segmentToTableSync():
    global segData
    global segmentComponentList
    segment = segmentInputVar.get()
    for index, segField in enumerate(segData):
        startIndex = segField[FIELD_INDEX] - 1
        endIndex = startIndex + segField[FIELD_SIZE]
        segBitValue = segment[startIndex:endIndex]
        segData[index][FIELD_VALUE] = segBitValue
        segmentComponentList[index][FIELD_VALUE][INPUT_COMPONENT_VAR].set(segBitValue)


def updateTable(pFrame):
    global segmentComponentList
    #     remove old form
    for component in segmentComponentList:
        component[FIELD_NAME].destroy()
        component[FIELD_INDEX].destroy()
        component[FIELD_SIZE].destroy()
        component[FIELD_VALUE][INPUT_COMPONENT].destroy()
        component[FIELD_VALUE][INPUT_COMPONENT_VAR].destroy()
    segmentComponentList = []
    #     create new form
    def updateVarValue(fieldIndex, compObj):
        global segData
        global segmentComponentList
        if len(compObj[FIELD_VALUE][INPUT_COMPONENT_VAR].get()) > segData[fieldIndex][FIELD_SIZE]:
            compObj[FIELD_VALUE][INPUT_COMPONENT_VAR].set(
                compObj[FIELD_VALUE][INPUT_COMPONENT_VAR].get()[:segData[fieldIndex][FIELD_SIZE]])
        # print("segField =" + str(segData[fieldIndex]))
        segData[fieldIndex][FIELD_VALUE] = compObj[FIELD_VALUE][INPUT_COMPONENT_VAR].get()
    for index, field in enumerate(segData):
        components = {}
        components[FIELD_NAME] = tkinter.Label(pFrame, text=field[FIELD_NAME])
        components[FIELD_NAME].grid(row=index, column=0, padx=10, pady=0)
        components[FIELD_INDEX] = tkinter.Label(pFrame, text="->" + str(field[FIELD_INDEX]))
        components[FIELD_INDEX].grid(row=index, column=1, padx=10, pady=0)
        components[FIELD_SIZE] = tkinter.Label(pFrame, text="[" + str(field[FIELD_SIZE]) + "]")
        components[FIELD_SIZE].grid(row=index, column=2, padx=10, pady=0)
        components[FIELD_VALUE] = {}
        components[FIELD_VALUE][INPUT_COMPONENT_VAR] = tkinter.StringVar(value=field[FIELD_VALUE])
        components[FIELD_VALUE][INPUT_COMPONENT] = tkinter.Entry(pFrame,
                                                                 textvariable=components[FIELD_VALUE][
                                                                     INPUT_COMPONENT_VAR],
                                                                 width=1 + field[FIELD_SIZE])
        components[FIELD_VALUE][INPUT_COMPONENT].grid(row=index, column=3, padx=10, pady=0, sticky="w")
        segmentComponentList.append(components)
        components[FIELD_VALUE][INPUT_COMPONENT_VAR].trace('w', lambda z, y, x, i=index, c=components: updateVarValue(i, c))


def updateOptions(pFrame):
    global optionComponents
    global segmentInputVar
    # destroy existing components
    for component in optionComponents:
        component.destroy()
    optionComponents = []
    # generate components
    # Segment Input / ToSegment, ToTable options
    segmentInputVar = tkinter.StringVar(value=segmentFromData())
    segmentInput = tkinter.Entry(pFrame,
         textvariable=segmentInputVar,
         width=1 + segData[len(segData) - 1][FIELD_INDEX] + segData[len(segData) - 1][FIELD_SIZE])
    segmentInput.grid(row=0, column=0, padx=20, pady=10)
    optionComponents.append(segmentInput)

    buttonsFrame = tkinter.Frame(optionsFrame)
    buttonsFrame.grid(row=1, column=0, padx=20, pady=20, sticky='w')

    segmentToTableButton  = tkinter.Button(buttonsFrame, text="Segment->Table", command=segmentToTableSync)
    segmentToTableButton.grid(row=0,column=0,padx=20,pady=10)
    tableToSegmentButton = tkinter.Button(buttonsFrame, text="Table->Segment", command=tableToSegmentSync)
    tableToSegmentButton.grid(row=0,column=1,padx=20,pady=10)

    optionComponents.append(segmentToTableButton)
    optionComponents.append(tableToSegmentButton)

def readFromSegDef():
    segData = []

    with open(os.path.join(root_path, 'segmentTables', fileName), 'r') as datasource_file:
        input_file = list(csv.DictReader(datasource_file, delimiter=delimiter))

    for vData in input_file:
        segDataField = {}
        indexStart = 0
        size = 0
        segDataField[FIELD_NAME] = vData["Ref"]
        # get segment size data
        if vData["SEG"].find("-") >= 0:
            range = vData["SEG"].split("-")
            indexStart = int(range[0])
            size = (int(range[1]) - int(range[0])) + 1
        else:
            indexStart = int(vData["SEG"])
            size = 1

        segDataField[FIELD_INDEX] = indexStart
        segDataField[FIELD_SIZE] = size
        segDataField[FIELD_VALUE] = vData["Example"]
        if segDataField[FIELD_VALUE] == None: segDataField[FIELD_VALUE] = ""
        segData.append(segDataField)
    return segData


def segmentFromData():
    segment = ""
    curIndex = 1
    for segField in segData:
        # For unspecified fields, add spaces
        if curIndex < int(segField[FIELD_INDEX]):
            segment = segment.ljust(segField[FIELD_INDEX] - 1)
            curIndex = segField[FIELD_INDEX]
        # Add field value to segment and pad with space
        segment += segField[FIELD_VALUE].ljust(segField[FIELD_SIZE])
        curIndex += segField[FIELD_SIZE]
    return segment


def writeAsSegment():
    segment = segmentFromData()
    with open(os.path.join(root_path, 'out', fileName + ".seg"), 'w') as dataDest_file:
        dataDest_file.writelines(segment)
    print("DONE")


#Frame = inner window
frame = tkinter.Frame(window)
tableFrame = tkinter.Frame(frame)
tableFrame.grid(row=0, column=0, padx=20, pady=20, sticky='w')
optionsFrame = tkinter.Frame(frame)
optionsFrame.grid(row=1, column=0, padx=20, pady=20, sticky='w')

#Work around for scroll box
frameTableDisplayOuter = tkinter.Frame(tableFrame)
frameTableDisplayOuter.pack(side='right', fill='both', expand=1)
tableDisplayCanvas = tkinter.Canvas(frameTableDisplayOuter, width=600)
tableDisplayCanvas.pack(side='left', fill='both', expand=1)
canvasScrollBar = ttk.Scrollbar(frameTableDisplayOuter, orient='vertical', command=tableDisplayCanvas.yview)
canvasScrollBar.pack(side="right", fill='y')
tableDisplayCanvas.configure(yscrollcommand=canvasScrollBar.set)
tableDisplayCanvas.bind('<Configure>',
                        # lambda e: tableDisplayCanvas.configure(scrollregion=(0,0,1000,3000)))
                        lambda e: tableDisplayCanvas.configure(scrollregion=tableDisplayCanvas.bbox('all')))
frameTableDisplayInner = tkinter.Frame(tableDisplayCanvas)
tableDisplayCanvas.create_window((0, 0), window=frameTableDisplayInner, anchor='nw')

# Read file
segData = readFromSegDef()
# Generate Table
updateTable(frameTableDisplayInner)
# Generate Buttons
updateOptions(optionsFrame)

# Read Segment Data
# Load Segment Data
# Save Segment Data
# Reset Defaults
frame.pack()
window.mainloop()
