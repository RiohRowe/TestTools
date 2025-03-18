from math import floor
from tkinter import messagebox as mb

from AirRowePy.GuiLibrary.FileManager import FileManager
from AirRowePy.GuiLibrary.ModalFrames.modalModules.EditCategoryFileModule import FILE_MANAGER, \
    FILE_NAME, FILE_EXT

fileManager = FileManager(FileManager.MAIN_LIST_FILES_PATH)
fileName = "chargeList"
fileExt = ".txt"

chargeListData = fileManager.loadTableFile(fileName+fileExt)
#sort in date order
DAY_IDX=1
MONTH_IDX=0
YEAR_IDX=2
def dateAAfterB(dateA, dateB):
    dateAMDY= dateA.split('/')
    dateBMDY= dateB.split('/')
    return (int(dateAMDY[YEAR_IDX])*500)+(int(dateAMDY[MONTH_IDX])*40)+int(dateAMDY[DAY_IDX])>(int(dateBMDY[YEAR_IDX])*500)+(int(dateBMDY[MONTH_IDX])*40)+int(dateBMDY[DAY_IDX])

def mergeSort(chargeListData):
    size=len(chargeListData)
    if size==1:
        return chargeListData
    split = floor(size/2)
    left=mergeSort(chargeListData[0:split])
    right=mergeSort(chargeListData[split:])
    sortedListData = []
    leftIdx=0
    rightIdx=0
    while len(sortedListData) < size:
        if leftIdx == len(left):
            sortedListData+=right[rightIdx:]
            break
        if rightIdx == len(right):
            sortedListData+=left[leftIdx:]
            break
        if dateAAfterB(left[leftIdx]["Date"], right[rightIdx]["Date"]):
            sortedListData.append(right[rightIdx])
            rightIdx+=1
        else:
            sortedListData.append(left[leftIdx])
            leftIdx+=1
    return sortedListData
#sort by date        
chargeListData = mergeSort(chargeListData)
#search for negative vals
removeIdxList = []
idx=0
for charge in chargeListData:
    if charge["Amount"].__contains__(','):
        charge["Amount"]=charge["Amount"].replace(',','')
    if charge["Name"].startswith("PAY_") and float(charge["Amount"])<0:
        res=mb.askquestion('Remove Charge?', str(charge))
        if res == 'yes' :
            removeIdxList.append(idx)
    idx+=1
for idx in removeIdxList.__reversed__():
    print("removing - "+str(chargeListData[idx]))
    chargeListData.pop(idx)
fileManager.saveTableFile(fileName+"V"+fileExt, chargeListData)