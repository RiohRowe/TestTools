from AirRowePy.GuiLibrary.FileManager import FileManager
from AirRowePy.GuiLibrary.ModalFrames.ModalWrapper import ModalWrapper
from AirRowePy.GuiLibrary.ModalFrames.modalModules.EditCategoryFileModule import EditCategoryFileModule, FILE_MANAGER, \
    FILE_NAME, FILE_EXT

def parseInText(parserStr, inText, values):
    checkVals = parserStr.split("%s")
    if len(checkVals) == 1:
        values.append(inText)
        return True
    inTextIdx = 0
    pcv = checkVals[0]
    if inText.startswith(pcv):
        inTextIdx = len(pcv)
    else:
        return False
    for checkVal in checkVals[1:]:
        inTextIdxNext = len(inText) if checkVal=="" else inText.find(checkVal, inTextIdx)
        if inTextIdxNext == -1:
            values.append(inText[inTextIdx:])
            return False
        else:
            values.append(inText[inTextIdx:inTextIdxNext])
            inTextIdx = inTextIdxNext+len(checkVal)
    return True

parserStr= "%s/%s/%s"
inText="03/17/2024"
values=[]
parseInText(parserStr,inText,values)