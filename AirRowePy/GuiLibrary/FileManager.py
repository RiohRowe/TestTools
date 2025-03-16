import csv
import os
from os import listdir
from os.path import isfile, join, abspath


class FileManager:
    def __init__(self, directoryPath):
        self.directoryPath = directoryPath
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
    def readFileToMap(self, myFileName, ext=None, rowDelim='\n', columnDelim='\t'):
        fullFilePath = self.findFilePath(myFileName, ext)
        if fullFilePath == None:
            return {}
        else:
            with open(fullFilePath, 'r') as mapFile:
                myMap = {}
                for line in mapFile.read().split(rowDelim):
                    print("["+line+"]")
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
                            elements.append(item)
                    return elements
                else:
                    elements = []
                    for line in lines:
                        for item in line.split(columnDelim):
                            elements.append(item)
                    return elements

    def loadTableFile(self, fileName, fileRootPath=None, columnDelimiter='\t'):
        with open(join(fileRootPath if fileRootPath else self.directoryPath, fileName), 'r') as datasource_file:
            return list(csv.DictReader(datasource_file, delimiter=columnDelimiter))

    def saveTableFile(self, fileName, listContents, fileRootPath=None, columnDelimiter='\t'):
        with open(join(fileRootPath if fileRootPath else self.directoryPath, fileName), 'w', newline='\n') as datasource_file:
            headers = list(listContents[0].keys()) if len(listContents) > 0 else []
            writer = csv.DictWriter(datasource_file, fieldnames=headers, delimiter=columnDelimiter)
            writer.writeheader()
            writer.writerows(listContents)
