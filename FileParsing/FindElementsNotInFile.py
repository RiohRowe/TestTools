readFileName = 'Batch-CFG_AGENCY_ORGANIZATION.csv'
searchElements = ["TX0430100","TX0310100","TX0570400","TX0430000","TX0570000","TXDPD0000","TX0430400","TX0571500","TX0030000","TX0030100","TX0030400","TX0370100","TX0370300","TX1130000","TX1130100","TX1210100","TX1740200","TX2020200","TX2100000","TX2280100","TXDPS1700","TX1080800","TX2200300","TX2200312","TX2200900","TX2201300","TX2201400","TX2201600","TX2201700","TX2202100","TX2202600","TX2203000","TX2203200","TX0571000","TX0572000","TX0572800","TX0574200","TX0910400","TX0990100","TX1990100","TXSPD0000","TX2000000","TX2200000","TX22000000","TX0140700","TX2200010","TX220013M","TX1120200","TX2120000","TX2120400"]

countResults = {}

with open(readFileName, 'r') as file:
    for line in file:
        for searchElement in searchElements:
            if not countResults.__contains__(searchElement):
                countResults[searchElement]=line.count(searchElement)
            else:
                countResults[searchElement] += line.count(searchElement)

for key, value in countResults.items():
    if value == 0:
        print(key +" has 0 occurances")