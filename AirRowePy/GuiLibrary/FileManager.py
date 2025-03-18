import csv
import os
from os import listdir
from os.path import isfile, join, abspath

# POINTS TO A FILE DIRECTORY
    # Allows writing and reading of contained files.

PATH_TO_ROOT = abspath(".")+"\\AirRowePy\\GuiLibrary\\"
class FileManager:
    # MAIN_LIST_FILES_PATH = "files/mainListFiles/"
    # TRANSLATION_MAP_FILES_PATH = "files/translationMaps/"
    # CATEGORY_FILES_PATH = "files/categoryFiles/"
    MAIN_LIST_FILES_PATH = "files\\mainListFiles\\"
    TRANSLATION_MAP_FILES_PATH = "files\\translationMaps\\"
    CATEGORY_FILES_PATH = "files\\categoryFiles\\"
    def __init__(self, directoryPath):
        self.directoryPath = PATH_TO_ROOT+directoryPath
    # Functions for finding file path.
    def getFilesNoExt(self):
        fileNames = [self.trimExt(fileName) for fileName in listdir(self.directoryPath) if isfile(join(self.directoryPath, fileName))]
        return fileNames
    def trimExt(self, fileName):
        if fileName.__contains__('.'):
            fileExtIdx = fileName.index('.')
            return fileName[0:fileExtIdx]
        return fileName
    def findFilePath(self, myFileName, ext=None):
        matchingFiles = [fileName for fileName in listdir(self.directoryPath) if fileName.startswith(myFileName)]
        if len(matchingFiles) == 1:
            return join(self.directoryPath, matchingFiles[0])
        elif len(matchingFiles) == 0:
            print ("fileNotFound. "+myFileName+" was not in directory "+abspath(self.directoryPath)+".\nOptions are: "+str(listdir(self.directoryPath)))
            return None
        else:
            for fileName in matchingFiles:
                if fileName.endswith(ext):
                    return join(self.directoryPath, fileName)

# MAP FILE FUNCTIONS
#
#   - Map files are of the below form and are used to map one value to another.
#       for instance, what my bank names a charge -> what I name the charge in my documents
#   ____ = tab_char
#   [originalVal1]____[mappedVal1]
#   [originalVal2]____[mappedVal2]
#   ...
#
    def readFileToMap(self, myFileName, ext=None, rowDelim='\n', columnDelim='\t'):
        fullFilePath = self.findFilePath(myFileName, ext)
        if fullFilePath == None:
            return {}
        else:
            myMap = {}
            with open(fullFilePath, 'r') as mapFile:
                for line in mapFile.read().split(rowDelim):
                    delimiterIdx = line.index(columnDelim)
                    myMap[line[0:delimiterIdx]] = line[delimiterIdx+1:]
            return myMap
    def writeMapToFile(self, fileName, mapValue, ext=None, rowDelim='\n', columnDelim='\t'):
        fullFilePath = self.findFilePath(fileName, ext)
        if fullFilePath == None:
            fullFilePath = join(self.directoryPath, fileName)
        file = open(fullFilePath, "w")
        count = len(mapValue)-1
        idx=0
        for key, value in mapValue.items():
            file.write(key+columnDelim+str(value))
            if idx < count:
                file.write(rowDelim)
                idx+=1
        file.close()

#CATEGORY_FILE FUNCTIONS
#   -Similar to the Table file, but each header has a different number of values in it.
#   Whereas a Table files are translated to a list of dicts with header-rowVal key-value pairs,
#   The Category files are translated to a dict with header-valueArr key-value pairs.
    def loadCategoryFile(self, fileName, ext=None, lineDelim='\n', columnDelim='\t'):
        fullFilePath = self.findFilePath(fileName, ext)
        if fullFilePath == None:
            return {}
        else:
            myCategories = {}
            with open(fullFilePath, 'r') as mapFile:
                lines = mapFile.read().split(lineDelim)
                if len(lines)==0:
                    return {}
                #read header line
                headers=lines[0].split(columnDelim)
                numCategories = len(headers)
                bodyData=[]
                for header in headers:
                    bodyData.append([])
                #read in category data
                for line in lines[1:]:
                    rowData = line.split(columnDelim)
                    for idx in range(0, numCategories):
                        val = rowData[idx]
                        if not val == "":
                            bodyData[idx].append(val)
                idx = 0
                for header in headers:
                    myCategories[header]= bodyData[idx]
                    idx+=1
            return myCategories
    def saveCategoryFile(self, fileName, data, ext=None, lineDelim='\n', columnDelim='\t'):
        fullFilePath = self.findFilePath(fileName, ext)
        if fullFilePath == None:
            fullFilePath = join(self.directoryPath, fileName)
        file = open(fullFilePath, "w")
        headers = list(data.keys())
        catLengths = {}
        file.write(columnDelim.join(headers))
        numLines = 0
        for header, valArr in data.items():
            arrSize = len(valArr)
            if arrSize > numLines:
                numLines=arrSize
            catLengths[header]=arrSize
        for rowIdx in range(0, numLines):
            file.write(lineDelim)
            lineVals = []
            for header in headers:
                if catLengths[header]<=rowIdx:
                    lineVals.append("")
                else:
                    lineVals.append(data[header][rowIdx])
            file.write(columnDelim.join(lineVals))
        file.close()


#TABLE_FILE_FUNCTIONS
#   -Table files are  just headered list files. They are used to track table like data and are of the below form:
#       ____ = tab_char
#   [Header1]____[Header2]____[Header3]...
#   [H1-Val1]____[H2-Val1]____[H3-Val1]...
#   [H1-Val2]____[H1-Val2]____[H3-Val2]...
#   ...

    def loadTableFile(self, fileName, fileRootPath=None, columnDelimiter='\t'):
        with open(join(fileRootPath if fileRootPath else self.directoryPath, fileName), 'r') as datasource_file:
            return list(csv.DictReader(datasource_file, delimiter=columnDelimiter))

    def saveTableFile(self, fileName, listContents, fileRootPath=None, columnDelimiter='\t'):
        with open(join(fileRootPath if fileRootPath else self.directoryPath, fileName), 'w', newline='\n') as datasource_file:
            headers = list(listContents[0].keys()) if len(listContents) > 0 else []
            writer = csv.DictWriter(datasource_file, fieldnames=headers, delimiter=columnDelimiter)
            writer.writeheader()
            writer.writerows(listContents)


# GENERAL FUNCTIONS
# pertain to any file type

    #   Reads any file to a list of values
    #       Optionally grabs only the first line (as headers)
    #       All but the first line (as body)
    #       or all lines (headerless files, like map files
    def readFileToList(self, myFileName, ext=None, headersOnly=False, bodyOnly=False, lineDelim='\n', columnDelim='\t'):
        fullFilePath = self.findFilePath(myFileName, ext)
        if fullFilePath == None:
            return []
        else:
            with open(fullFilePath, 'r') as optionFile:
                lines = optionFile.read().split(lineDelim)
                if len(lines)==0:
                    return []
                if headersOnly:
                    return lines[0].split(columnDelim)
                elif bodyOnly:
                    elements = []
                    for line in lines[1:]:
                        for item in line.split(columnDelim):
                            if not item == "": #IGNORE BLANK ENTRIES
                                elements.append(item)
                    return elements
                else:
                    elements = []
                    for line in lines:
                        for item in line.split(columnDelim):
                            if not item == "": #IGNORE BLANK ENTRIES
                                elements.append(item)
                    return elements