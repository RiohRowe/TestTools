# readFileName = 'Batch-CFG_AGENCY_ORGANIZATION.csv'
readFileName = 'out.txt'
countResults = {}

with open(readFileName, 'r') as file:
    # with open("out.txt", 'w') as outFile:
        for line in file:
            # uwslcLine = line.lower().replace(" ","").replace("\t","").replace("\n","")
            uwslcLine = line
            if not countResults.__contains__(uwslcLine):
                countResults[uwslcLine]=1
                # outFile.write(line)
            else:
                countResults[uwslcLine] += 1

count = 0
for key, value in countResults.items():
    if value > 1:
        count +=1
        print(key +" is Duplicated "+str(value)+" times")
print("num="+str(count))