from AirRowePy.GuiLibrary.FileManager import FileManager
from AirRowePy.GuiLibrary.ModalFrames.ModalWrapper import ModalWrapper
from AirRowePy.GuiLibrary.ModalFrames.modalModules.EditCategoryFileModule import EditCategoryFileModule, FILE_MANAGER, \
    FILE_NAME, FILE_EXT

def buildOutText(builderStr, values):
    if builderStr == "":
        return "".join(values)
    subStrs = []
    for idx in range(0,len(values)):
        subStrs.append("%s"+str(idx))
    print("builderStr="+builderStr+"\nvalues=\t"+str(values)+"\nsubstr=\t"+str(subStrs))
    for idx in range(len(values)-1, -1, -1):
        builderStr=builderStr.replace(subStrs[idx], values[idx])
    return builderStr
apple = "apple"
apple = apple.replace("pp","dd")
print(apple)
builderStr= "%s2/%s0/%s1"
inText="03/17/2024"
values=["03","17","2024"]
print(buildOutText(builderStr,values))