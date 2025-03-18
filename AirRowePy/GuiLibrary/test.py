from AirRowePy.GuiLibrary.FileManager import FileManager
from AirRowePy.GuiLibrary.ModalFrames.ModalWrapper import ModalWrapper
from AirRowePy.GuiLibrary.ModalFrames.modalModules.EditCategoryFileModule import EditCategoryFileModule, FILE_MANAGER, \
    FILE_NAME, FILE_EXT

fileData={
    FILE_MANAGER:FileManager(FileManager.CATEGORY_FILES_PATH),
    FILE_NAME:"chargeAssociations",
    FILE_EXT:None
}

unmappedVals = ["one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty","twentyone","twentytwo","twentythree","twentyfour","twentyfive","twentysix"]

modal = ModalWrapper(EditCategoryFileModule, "CategoryEditing", elements=unmappedVals, otherOptions=fileData, handleResolveValue=lambda *args, value, cM={}:print(value))