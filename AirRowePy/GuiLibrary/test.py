from AirRowePy.GuiLibrary.FileManager import FileManager
from AirRowePy.GuiLibrary.ModalFrames.ModalWrapper import ModalWrapper
from AirRowePy.GuiLibrary.ModalFrames.modalModules.EditCategoryFileModule import EditCategoryFileModule, FILE_MANAGER, \
    FILE_NAME, FILE_EXT

unmappedVals=["one","two","three","four","five","six","seven","eight","nine"]
fileManager = FileManager(FileManager.CATEGORY_FILES_PATH)
fileName="chargeAssociations"
fileExt="txt"

fileOptions={
    FILE_MANAGER:fileManager,
    FILE_NAME:fileName,
    FILE_EXT:fileExt
}

modal = ModalWrapper(EditCategoryFileModule, "CategoryEditing", elements=unmappedVals, otherOptions=fileOptions)