import os.path

from AirRowePy.GuiLibrary.ModalFrames.ModalWrapper import ModalWrapper
from AirRowePy.GuiLibrary.ModalFrames.modalModules.AddToListModalComponents.AssignValuesModal.AssignValuesToMapModal import \
    AssignValuesToMapModal
from AirRowePy.GuiLibrary.ModalFrames.modalModules.baseAddToListModalModule import BaseAddElementsModalModule
from AirRowePy.GuiLibrary.WindowWrapper import RootWindow
from AirRowePy.GuiLibrary.Frames.EditableStringListFromCsvFile import EditableStringListFromFileComponent

window = RootWindow("Hello World")
mainFrame = window.getRoot()
list = EditableStringListFromFileComponent(mainFrame, "ChargeList", fileName='chargeList.txt', fileDelimiter='\t', rangeEnd=0, rangeSize=4)
window.show()

# modal = ModalWrapper(BaseAddElementsModalModule, "SomeModal", elements=[
#     {"h1":{"type": "t", "editable": True, "defaultValue": "defaultValue1"},"h2":{"type": "t", "editable": False, "defaultValue": "defaultValue2"}},
#     {"h1":{"type": "t", "editable": True, "defaultValue": "defaultValue3"},"h2":{"type": "t", "editable": False, "defaultValue": "defaultValue4"}},
#     {"h1":{"type": "t", "editable": True, "defaultValue": "defaultValue5"},"h2":{"type": "t", "editable": True, "defaultValue": "defaultValue6"}},
#     {"h1":{"type": "t", "editable": True, "defaultValue": "defaultValue7"},"h2":{"type": "t", "editable": True, "defaultValue": "defaultValue8"}}
# ])

# modal = ModalWrapper(AssignValuesToMapModal, "EditMapModal", elements=rowMap, handleResolveValue=self.fm.writeMapToFile)
# modal = ModalWrapper(AssignValuesToMapModal, "SomeModal", elements={
#     "apple":"",
#     "pear":"",
#     "peach":"",
#     "plumb":"",
#     "apricott":""
# })

# objList = [{
#     "thing1":{"S1":"h", "S2":"e", "S3":"l"},
#     "thing2":{"S1":"l", "S2":"o", "S3":"_"},
#     "thing3":{"S1":"w", "S2":"o", "S3":"r"}
# },{
#     "thing1":{"S1":"l", "S2":"d", "S3":"_"},
#     "thing2":{"S1":"h", "S2":"o", "S3":"w"},
#     "thing3":{"S1":"_", "S2":"r", "S3":"u"}
# }]
#
# for idx, headers in enumerate(objList):
#     for hidx, header in enumerate(headers.keys()):
#         print(str(idx) + " - " + str(hidx) + " = " + header)
#         print(headers[header]["S1"]+headers[header]["S2"]+headers[header]["S3"])
